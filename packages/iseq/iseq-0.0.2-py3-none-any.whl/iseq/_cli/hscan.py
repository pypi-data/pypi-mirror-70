import os
from typing import IO, Optional

import click
from fasta_reader import FASTAWriter, open_fasta
from hmmer_reader import open_hmmer

from iseq.alphabet import infer_fasta_alphabet, infer_hmmer_alphabet
from iseq.model import EntryDistr


@click.command()
@click.argument("profile", type=click.File("r"))
@click.argument("target", type=click.File("r"))
@click.option(
    "--epsilon", type=float, default=1e-2, help="Indel probability. Defaults to 1e-2."
)
@click.option(
    "--output",
    type=click.File("w"),
    help="Save results to OUTPUT (GFF format).",
    default=os.devnull,
)
@click.option(
    "--ocodon",
    type=click.File("w"),
    help="Save codon sequences to OCODON (FASTA format).",
    default=os.devnull,
)
@click.option(
    "--oamino",
    type=click.File("w"),
    help="Save amino acid sequences to OAMINO (FASTA format).",
    default=os.devnull,
)
@click.option(
    "--quiet/--no-quiet", "-q/-nq", help="Disable standard output.", default=False,
)
@click.option(
    "--window",
    type=int,
    help="Window length. Defaults to zero, which means no window.",
    default=0,
)
@click.option(
    "--hmmer3-compat/--no-hmmer3-compat",
    help="Enable full HMMER3 compatibility. Defaults to False.",
    default=False,
)
@click.option(
    "--entry-distr",
    type=click.Choice(["uniform", "occupancy"], case_sensitive=False),
    help="Set the entry distribution. Defaults to occupancy.",
    default="occupancy",
)
def hscan(
    profile,
    target,
    epsilon: float,
    output,
    ocodon,
    oamino,
    quiet,
    window: int,
    hmmer3_compat: bool,
    entry_distr: str,
):
    """
    Search nucleotide sequence(s) against a protein profiles database.

    An OUTPUT line determines an association between a TARGET subsequence and
    a PROFILE protein profile. An association maps a target subsequence to a
    profile and represents a potential homology. Expect many false positive
    associations as we are not filtering out by statistical significance.
    """
    from .scanner import OutputWriter
    from .hmmer3_scanner import HMMER3Scanner

    owriter = OutputWriter(output, epsilon, window)
    FASTAWriter(ocodon)
    FASTAWriter(oamino)

    if entry_distr == "occupancy":
        edistr = EntryDistr.OCCUPANCY
    else:
        edistr = EntryDistr.UNIFORM

    if quiet:
        stdout = click.open_file(os.devnull, "a")
    else:
        stdout = click.get_text_stream("stdout")

    profile_abc = _infer_profile_alphabet(profile)
    target_abc = _infer_target_alphabet(target)

    scanner: Optional[HMMER3Scanner] = None

    if profile_abc.symbols != target_abc.symbols:
        raise click.UsageError("Alphabets mismatch.")

    scanner = HMMER3Scanner(owriter, window, stdout, hmmer3_compat, edistr)

    with open_fasta(target) as fasta:
        targets = list(fasta)

    for hmmprof in open_hmmer(profile):
        scanner.show_profile_parser(hmmprof)
        scanner.process_profile(hmmprof, targets)

    scanner.finalize_stream("output", output)
    scanner.finalize_stream("ocodon", ocodon)
    scanner.finalize_stream("oamino", oamino)


def _infer_profile_alphabet(profile: IO[str]):
    hmmer = open_hmmer(profile)
    hmmer_alphabet = infer_hmmer_alphabet(hmmer)
    profile.seek(0)
    if hmmer_alphabet is None:
        raise click.UsageError("Could not infer alphabet from PROFILE.")
    return hmmer_alphabet


def _infer_target_alphabet(target: IO[str]):
    fasta = open_fasta(target)
    target_alphabet = infer_fasta_alphabet(fasta)
    target.seek(0)
    if target_alphabet is None:
        raise click.UsageError("Could not infer alphabet from TARGET.")
    return target_alphabet
