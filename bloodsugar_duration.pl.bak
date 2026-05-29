#!/usr/bin/perl
use strict;
use warnings;

my(@lines,@extralines);
open my $fh, '<', 'bloodsugar.md' or die "Cannot open bloodsugar.md: $!";
my$total=0;my$t=0;my$tmpn=0;my$tmpt=0;my$tmpa=0;my$tmpb=0;
foreach(reverse<$fh>){
	if(/(`\{\d\d:)|(####)/ && $t<2){
		push@lines,$_ ;
		$tmpn++ if /(<|>)内/;
		$tmpt++ if /(<|>)T/;
		$tmpa++ if /(<|>)A/;
		$tmpb++ if /(<|>)B/;
		$t++ if /####/;
	}
	if($t>=2 && $tmpn>=1 && $tmpt>=1 && $tmpa>=1 && $tmpb>=1){
		last;
	}elsif($t>=2){
		#print;
		push@extralines,$_ and $tmpn++ if /(<|>)(内)/ && $tmpn==0;
		push@extralines,$_ and $tmpt++ if /(<|>)(T)/ && $tmpt==0;
		push@extralines,$_ and $tmpa++ if /(<|>)(A)/ && $tmpa==0;
		push@extralines,$_ and $tmpb++ if /(<|>)(B)/ && $tmpb==0;
	}
}
#print foreach @lines;print"\n";
#print"total_mark=$t_mark, total=$total\n";

foreach(reverse @extralines){
	s/    - `\{\d\d:\d\d /      {/g;
	s/}`/}/g;
	s/((<|>)(内|T|A))/\e[1;37;41m$1\e[0m/g;
	print;
}

#print"@extralines";
@lines=reverse@lines;
#print foreach @lines;print"\n";
#print"\n$#lines\n";

#__END__
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
    print "$time[$i] {$dosage[$i]} $duration[$i]";
	print "\n" unless $i==$#dosage;
    if ($i == $d1 - 1) { 
        if($i==$#dosage){
           print"\n";
           print "#### $date[1]$week[1]"
    }else{
        print "#### $date[1]$week[1]\n"
    }

 #       print "\n" if $i==$#dosage;
   # Print second heading when reaching the split point
 #       print "#### $date[1]$week[1]\n";
    }
}