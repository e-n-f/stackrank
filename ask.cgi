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
	($tlid, $end, $loc1, $loc2, $ang, $url, $url2) = split(/ /);

	$url{"$tlid$end"} = $url;
	$url2{"$tlid$end"} = $url2;
}
close(IN);
open(IN, "/home/enf/stackrank/urls2");
while (<IN>) {
	chomp;
	($tlid, $end, $loc1, $loc2, $ang, $url, $url2) = split(/ /);

	$url{"$tlid$end"} = $url;
	$url2{"$tlid$end"} = $url2;

	$eb{"$tlid$end"} = 1;
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
	# @k2 = keys(%eb);
	$k2 = $k2[rand($#k2)];

	$k2 = $k1[rand($#k1)];

	if (! -s "/var/www/tlid/$k1.jpg") {
		system "curl -q -m60 -L -o /var/www/tlid/$k1.jpg '$url{$k1}'";
	}
if (0) {
	if (! -s "/var/www/tlid/${k1}a.jpg") {
		system "curl -q -m60 -L -o /var/www/tlid/${k1}a.jpg '$url2{$k1}'";
	}
}

	if (! -s "/var/www/tlid/$k2.jpg") {
		system "curl -q -m60 -L -o /var/www/tlid/$k2.jpg '$url{$k2}'";
	}
if (0) {
	if (! -s "/var/www/tlid/${k2}a.jpg") {
		system "curl -q -m60 -L -o /var/www/tlid/${k2}a.jpg '$url2{$k2}'";
	}
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

print "Which place is more alive?";

print "<form action='/cgi-bin/ask.cgi' method='post'>\n";
print "<input type='hidden' name='tlid1' value='$k1'>\n";
print "<input type='hidden' name='tlid2' value='$k2'>\n";

# print "<table><tr><td>";

print "<img src='/tlid/$k1.jpg'> ";
# print "<img src='/tlid/${k1}a.jpg'> ";
# print "<p>";
print "<input type='Submit' name='pref' value='First'>\n";
print "<input type='Submit' name='pref' value='Reject&#160;First'>\n";
# print "</td><td>";
print "<p>\n";
print "<img src='/tlid/$k2.jpg'> ";
# print "<img src='/tlid/${k2}a.jpg'> ";
# print "<p>\n";
print "<input type='Submit' name='pref' value='Second'>\n";
print "<input type='Submit' name='pref' value='Reject&#160;Second'>\n";
# print "</td></tr>";

print "</form>\n";
