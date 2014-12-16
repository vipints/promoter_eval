#!/usr/bin/env perl
#	Description: - read fixedStep or variableStep wiggle input data,
#		output four column bedGraph format data
#   Author: Vipin

use warnings;
use strict;

my ($position, $chr, $step, $span) = (0, "", 1, 1);

my $usage = q(
fstep_to_bed.pl  - Program to convert a valid fixedStep or variableStep wiggle input data to BED format.
USAGE: fstep_to_bed.pl <fixedStep/variableStep Wiggle format> +/- > <output file name>

);

if (scalar(@ARGV) != 2) {
    print $usage;
    exit
}

my $inFile = $ARGV[0];
my $strand = $ARGV[1];

open WIG, "<$inFile" || die "Can't open the Wiggle file \n";
while (my $dataValue = <WIG>)
#while (my $dataValue = <STDIN>)
{
    chomp $dataValue;
    if ( $dataValue =~ m/^track /) {
        print STDERR "Skipping track line\n";
        next;
    }
    if ( $dataValue =~ m/^fixedStep/ || $dataValue =~ m/^variableStep/ ) {
        $position = 0;
        $chr = "";
        $step = 1;
        $span = 1;
        my @a = split /\s/, $dataValue;
        for (my $i = 1; $i < scalar(@a); ++$i) {
            my ($ident, $value) = split('=',$a[$i]);
            if ($ident =~ m/chrom/) { $chr = $value; }
            elsif ($ident =~ m/start/) { $position = $value-1; }
            elsif ($ident =~ m/step/) { $step = $value; }
            elsif ($ident =~ m/span/) { $span = $value; }
            else {
                print STDERR "ERROR: unrecognized fixedStep line: $dataValue\n";
                exit 255;
            }
        }
        open WIG, ">$chr" || die "Can't open for writing\n";
    } 
    else {
        my @b = split('\s', $dataValue);
        if (scalar(@b)>1) {
            $position = $b[0];
            $dataValue = $b[1];
        }
        my $loc_pos = $position+$span;
        print "$chr\t$position\t$loc_pos\t$dataValue\t$strand\n";
        $position = $position + $step;
    }
}
close WIG;
exit;
