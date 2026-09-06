#!/usr/bin/perl
use strict;
use warnings;
use File::Basename qw(basename);
#use File::Copy qw(copy);

my$file="bloodsugar.md";
#my$phone_img_folder="/home/louisophie/Downloads/github/BG_record/image.bak";
my$phone_img_folder="/data/data/com.termux/files/home/storage/shared/DCIM/Camera";
#<magic begin
@_ = glob("${phone_img_folder}/*.jpg");
$_ = (sort { -M $a <=> -M $b } @_)[0];
my$img_name=basename($_) ;
#system("jpegoptim", "-v", "-d", "./image/", "--size=100k", "--strip-all", "-o", "$_") == 0 or die "jpegoptim failed: $?";
system("magick", "$_", "-resize", "20%", "-strip", "-quality", "80", "-monitor", "./image/$img_name") == 0 or die "magick failed: $?";
print "proceed? [Enter=yes, Ctrl-C=abort] ";<STDIN>;
#>magic end

#<find the line-number begin
my $line;
open my $fh, '<', "$file" or die "Cannot open $file: $!";
while(<$fh>){
	if(/^###/ || /^\d+\. \d\d:/ || /^ +?- +?`\{/){
			$line = $.;
			#END
		}
}
close $fh;
#>find the line-number end

#<insert an img to the bloodsugar.md with .bak
if (defined $line) {
    local $^I = ".bak";          # backup; set to "" for no backup
    local @ARGV = ($file);
    while(<>){
        s/$/ ![${img_name}](.\/image\/${img_name})/ if $. == $line;
        print;
    }
}
system("cat", "-n", "$file");

__END__
`
git add "./image/$img_name" bloodsugar.md
git commit -m "$(date +%Y%m%d%a%H:%M)_A5pro"
git push
echo "Done"
`
