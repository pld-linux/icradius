package ICRadiusCFG;

##  # important values from /etc/raddb/radius.conf:
##  server localhost
##  login radius
##  password radius
##  radius_db radius

my $radius_conf = "/etc/raddb/radius.conf";

open IN,"< $radius_conf" || die "Error reading $radius_conf";

while(<IN>) {
   chomp $_;
   if (( $_ =~ /^#/ ) || ( $_ =~ /^\ *$/))
      { next; }
   elsif (/^(\w+)\s(\w+)$/) {
      my $k=$1;
      my $v=$2;
      if ($k eq "server")
         { our $dbhost = $v; }
      elsif ($k eq "radius_db")
         { our $dbname = $v; }
      elsif ($k eq "login")
         { our $dbusername = $v; }
      elsif ($k eq "password")
         { our $dbpassword = $v; }
   }
}
close IN;

1;
__END__
