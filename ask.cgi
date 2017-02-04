#!/usr/bin/perl

while (<>) {
        $query .= $_;
}
@vars = split(/&/, $query);

print "Content-type: text/html\n\n";

for $v (@vars) {
        ($key, $val) = split(/=/, $v, 2);
        $val =~ s/%20/ /g;
        $val =~ s/%2C/,/g;

        $val =~ s/[^A-Za-z0-9._,: -]//g;

        $var{$key} = $val;
}

if ($var{'pref'} ne "") {
        open(OUT, ">>/home/enf/stackrank/asked");
        $time = time;
        print OUT "$var{'tlid1'} $var{'tlid2'} $var{'pref'} $ENV{'REMOTE_ADDR'} $time\n";
        close(OUT);
}

open(IN, "/home/enf/stackrank/urls");
while (<IN>) {
	chomp;
	($tlid, $end, $loc1, $loc2, $ang, $url) = split(/ /);

	$url{"$tlid$end"} = $url;
}
close(IN);

open(IN, "/home/enf/stackrank/asked");
while (<IN>) {
	chomp;
	($tlid, $tlid2) = split(/ /);
	$asked{"$tlid"} = 1;
	$asked{"$tlid2"} = 1;
}
close(IN);

while (1) {
	@k1 = keys(%asked);
	$k1 = $k1[rand($#k1)];

	@k2 = keys(%url);
	$k2 = $k2[rand($#k2)];

	if (! -s "/var/www/tlid/$k1.jpg") {
		system "curl -q -m60 -L -o /var/www/tlid/$k1.jpg '$url{$k1}'";
	}

	if (! -s "/var/www/tlid/$k2.jpg") {
		system "curl -q -m60 -L -o /var/www/tlid/$k2.jpg '$url{$k2}'";
	}

	($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size, $atime,$mtime,$ctime,$blksize,$blocks) = stat("/var/www/tlid/$k1.jpg");
	if ($size < 10000) {
		next;
	}
	($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size, $atime,$mtime,$ctime,$blksize,$blocks) = stat("/var/www/tlid/$k2.jpg");
	if ($size < 10000) {
		next;
	}
	last;
}

print "<form action='/cgi-bin/ask.cgi' method='post'>\n";
print "<input type='hidden' name='tlid1' value='$k1'>\n";
print "<input type='hidden' name='tlid2' value='$k2'>\n";

print "<table><tr><td>";

print "<img src='/tlid/$k1.jpg'>";
print "<p>";
print "<input type='Submit' name='pref' value='First'>\n";
print "</td><td>";
print "<img src='/tlid/$k2.jpg'>";
print "<p>\n";
print "<input type='Submit' name='pref' value='Second'>\n";
print "</td></tr>";

print "</form>\n";
