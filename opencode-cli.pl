#!/usr/bin/perl
use strict;
use warnings;
use open ':std', ':encoding(UTF-8)';
use utf8;
binmode STDOUT, ':utf8';
use Term::ANSIColor qw(colored color);
use JSON::PP qw(decode_json);

$|=1;
our $in_code=0; # before loop, not inside sub
our $in_diff=0; # unified-diff block state for TUI-like colors
our $diff_file=''; # filename of current diff (from Index line)

# --- diff filepath -> just the basename, shortened ---
sub shortpath {
  my($p)=@_;
  $p =~ s{.*/github/BG_record/}{} or $p =~ s{.*/}{};
  return $p;
}

sub md2ansi {
  my($s)=@_;
  $s =~ s/\e\[\?[0-9;]*[uUlh]//g;
  $s =~ s/\e\[[0-9;?]*\$p//g;
  $s =~ s/\e\].*?(?:\a|\e\\)//g;
  my $nl = ($s =~ s/(\r?\n)$//) ? $1 : '';
  # --- TUI-like headers ---
  if($s =~ /^Thought\s*[·.]\s*.*$/) { return colored($s.$nl,'yellow'); }
  if($s =~ /^\s*(←|<-)\s*Edit\s+(.*?)\s*$/) { $in_diff=1; $diff_file=$2; return colored("← Edit ".shortpath($2).$nl,'bold bright_white'); }
  # --- parse unified-diff metadata (suppress the noise) ---
  if($s =~ /^Index:\s+(.+)$/) { $in_diff=1; $diff_file=$1; return ""; }          # suppress, capture file
  if($s =~ /^=+$/) { return ""; }                                                # suppress divider
  if($s =~ /^---\s/) { return ""; }                                              # suppress
  if($s =~ /^\+\+\+\s/) { return ""; }                                           # suppress
  if($s =~ /^@@\s.*@@/) { $in_diff=1; return colored("┌ ".$s.$nl,'bright_black'); }  # keep hunk marker, dim
  # --- inside diff block ---
  if($in_diff) {
    # prose line ends diff -> fall through to markdown
    unless($s =~ /^[ \@\+\-]/ || $s =~ /^\s*\d+\./ || $s =~ /^\s*[-+]\s*`/ || $s eq '') {
      $in_diff=0;
      my $lab = $diff_file ? " ─ ".shortpath($diff_file) : "";
      return colored("└──".$lab.$nl,'bright_black');
    }
  }
  if($in_diff) {
    if($s =~ /^\s*$/) { return $s.$nl; }
    if($s =~ /^\+(.*)$/s) {
      my $rest=$1;
      $rest =~ s/`([^`\n]+?)`/"\e[1;38;5;120;48;5;23m$1\e[0m\e[48;5;23m"/ge;
      $rest =~ s/\*\*(.+?)\*\*/"\e[1;97;48;5;23m$1\e[0m\e[48;5;23m"/ge;
      $rest =~ s/(^|\s)(\d+\.)/$1."\e[33;1;48;5;23m$2\e[0m\e[48;5;23m"/ge;
      return "\e[48;5;23m\e[33;1m+\e[0m\e[48;5;23m".$rest."\e[0m".$nl;
    }
    if($s =~ /^\-(?!\-\-)(.*)$/s) {
      my $rest=$1;
      $rest =~ s/`([^`\n]+?)`/colored($1,'bold red')/ge;
      return colored('-','bold red').colored($rest.$nl,'red');
    }
    # context ' ' line -> TUI-like: numbers yellow, code green
    my $c=$s;
    $c =~ s/`([^`\n]+?)`/colored($1,'green')/ge;
    $c =~ s/(^|\s)(\d+\.)/$1.colored($2,'yellow')/ge;
    return $c.$nl;
  }
  if($s=~/^```/){ $in_code=!$in_code; return colored($s.$nl,'bright_black'); }
  return colored($s.$nl,'green') if $in_code;
  $s =~ s/`([^`\n]+?)`/colored($1,'green')/ge;
  $s =~ s/\*\*(.+?)\*\*/colored($1,'bold bright_white')/ge;
  $s =~ s/(?<!\w)\*(?!\s)([^*\n]+?)(?<!\s)\*(?!\w)/colored($1,'italic yellow')/ge;
  $s =~ s/^(\s*)[\*\-]\s+/$1.'  '.colored('•','green').' '/gme;
  return $s.$nl;
}

my $m1=colored('█▀▀█  OpenCode','blue');
my $m2=colored('█  █  CLI in perl','blue');
my $m3=colored('▀▀▀▀','blue');
my $m4=colored('▣','blue');
print"\n$m1\n$m2\n$m3\n$m4 ";
while(<STDIN>){
  $in_code=0; $in_diff=0;
  chomp; next unless /\S/;
  local $ENV{TERM}='xterm-256color';
  open my $null,'<','/dev/null' or die $!;
  local *STDIN = $null;
  open my $fh,'-|','opencode','run','-c','--',$_ or warn $! and next;
  while(my $l=<$fh>){ print md2ansi($l); }
  close $fh;
  print color('reset'),"\n";
  print "\e[<u\e[?1000l\e[?1002l\e[?1003l\e[?1006l\n$m4 ";
}

__END__
#print <<'LOGO';
█▀█ █▀█ █▀▀ █▀▄ █▀▀ █▀█ █▀▄ █▀▀
█▄█ █▀▀ █▀▀ █▄▀ █▄▄ █▄█ █▄▀ █▄▄
#LOGO
8