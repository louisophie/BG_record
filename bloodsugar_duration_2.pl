#!/usr/bin/perl
use strict;
use warnings;

my@lines;
open my $fh, '<', 'bloodsugar.md' or die "Cannot open bloodsugar.md: $!";
my$t=0;
foreach(reverse<$fh>){
	next if /^$/ || /---/;     # skip empty lines and lines containing ---
	#print;
	push@lines,$_;
	$t++ if /####/;
	last if $t==2;
}
@lines=reverse@lines;
#print foreach @lines;print"\n";
#__END__
my($date,$d,$d1);
my$d2=0;
my(@date,@week,@lines_of_duration,@time,@date_time,@date_time_dosage,@dosage,@time_dosage);
foreach(@lines){
	if(/^#### (\d+)(.+)/){
		$date=$1;
		push(@date,$date);
		push(@week,$2);
		$d++;
	}
	#my$date=$1 if /^#### (\d+)/;
	if(/`\{(\d\d:\d\d) (.+)\}`/){
		push (@lines_of_duration,$d2);	#e.g., 2nd of @lines_of_duration is the 5th line of @lines
		push (@date_time,"$date $1");
		push (@time,$1);
		#push (@date_time_dosage,"$date $1 $2");
		#push (@time_dosage,"$1 $2");
		push (@dosage,$2);
		$d1++ if $d==1;
	}
	$d2++;
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

$t=0;
foreach my$i (@lines_of_duration){	#$i==line number of /`\{(\d\d:\d\d) (.+)\}`/ in @lines, $t == line number of @lines_of_duration, @duration, @date_time, @time and @dosage
    $lines[$i] =~ s/((<|>)(内|T|A))/\e[1;37;41m$1\e[0m/g;    # Highlight < > 内 T A in red background
	if($lines[$i] =~ /((T|I)(>|<))|(T|I)\e\[1;37;41m(>|<)/){
		$lines[$i] =~ s/(`\{.+\}`)/\e[1;4m$1\e[0m/g;
		$duration[$t] = "\e[1;4m$duration[$t]\e[0m";
	}
	$lines[$i]=~s/^ +- //;
    $lines[$i]="$duration[$t]\t$lines[$i]";
	#$lines[$_].=" $duration[$t]\n";
	#print"$lines[$_]";
	$t++;
}
foreach(@lines){
	#chomp;
	s/^(\d+.) / $1/;
	chomp if $_ eq $lines[-1];
	print;
}
