#!/usr/bin/perl
use strict;
use warnings;

my ($red, $blue) = (shift, shift);

my $server = "localhost"; # also try: server.megaminerai.com
my $game   = 1000 + int rand 1000000;

#print "Running match of $red vs $blue\n";

# Red game
chdir($red);
open RED, "./run $server $game |" or die "Couldn't open red at ./$red/run: $!\n";
chdir("..");

# Blue game
chdir($blue);
open BLUE, "./run $server $game |" or die "Couldn't open blue at ./$blue/red: $!\n";
chdir("..");

while (<RED>) {
	print $red if ($_ =~ /You Win/i);
	print $blue if ($_ =~ /You Lose/i);
}

close RED;
close BLUE;
