#!/usr/bin/perl
use strict;
use warnings;

my@lines;
open my $fh, '<', 'bloodsugar.md' or die "Cannot open bloodsugar.md: $!";
my$t=0;
foreach(reverse<$fh>){
	#print;
	push@lines,$_ if /(`\{\d\d:)|(####)/;
	$t++ if /####/;
	last if $t==2;
}
@lines=reverse@lines;
#print foreach @lines;print"\n";
#print"\n$#lines\n";

my($date,$d,$d1,$d2);
my(@date,@week,@time,@date_time,@date_time_dosage,@dosage,@time_dosage);
foreach(@lines){
	if(/^#### (\d+)(.+)/){
		$date=$1;
		push(@date,$date);
		push(@week,$2);
		$d++;
	}
	#my$date=$1 if /^#### (\d+)/;
	if(/`\{(\d\d:\d\d) (.+)\}`/){
		push (@date_time,"$date $1");
		push (@time,$1);
		#push (@date_time_dosage,"$date $1 $2");
		#push (@time_dosage,"$1 $2");
		push (@dosage,$2);
		$d1++ if $d==1;
	}
}

my@seconds;	#make it keep going up.
foreach(0..$#date_time){
	chomp(my$s1=`date -d "$date_time[$_]" +%s 2>/dev/null`);
	push(@seconds,$s1);
}
foreach(0..$#seconds-1){
	$seconds[$_+1] += 86400 if $seconds[$_+1] -$seconds[$_] < 0;
}
#print and print"\n" foreach @seconds;
my@duration;
foreach(@seconds){
	my $diff = time() - $_;
	push(@duration,sprintf("%02d:%02d",int($diff / 3600), int(($diff % 3600) / 60)));
}
#print and print"\n" foreach(@duration);

print "#### $date[0]$week[0]\n";
foreach my $i (0 .. $#dosage) {
    $dosage[$i] =~ s/((<|>)(内|T|A))/\e[1;37;41m$1\e[0m/g;    # Highlight < > 内 T A in red background
    if ($dosage[$i] =~ /((T|I)(>|<))|(T|I)\e\[1;37;41m(>|<)/) {
        $dosage[$i]  = "\e[1;4m$dosage[$i]\e[0m";
        $duration[$i] = "\e[1;4m$duration[$i]\e[0m";
    }    # Underline if it contains T/I with < or >
    print "$time[$i] {$dosage[$i]} $duration[$i]\n";
    if ($i == $d1 - 1) {    # Print second heading when we reach the split point
        print "#### $date[1]$week[1]\n";
    }
}