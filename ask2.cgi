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
        open(OUT, ">>/home/enf/stackrank/asked2");
        $time = time;
        print OUT "$var{'tlid1'} $var{'tlid2'} $var{'pref'} $ENV{'REMOTE_ADDR'} $time\n";
        close(OUT);
}

open(IN, "/home/enf/daily.csv");
while (<IN>) {
        chomp;
        @fields = split(/,/);

        $lat = $fields[25];
        $lon = $fields[26];
        next if ($lat eq "");
	next if $seen{"$lat,$lon"};
	$seen{"$lat,$lon"} = 1;

        $walk = 0;
        $drive = 0;
        for ($i = 5; $i < 5 + 12; $i++) {
                $drive += $fields[$i];
        }
        for ($i = 5 + 12; $i < 5 + 12 + 4; $i++) {
                $walk += $fields[$i];
        }

        if ($drive < 200 || $walk < 750) {
                next;
        }

        $url{"$lat,$lon,$walk,$drive"} = "https://maps.googleapis.com/maps/api/streetview?size=640x300&fov=90&location=$lat,$lon&heading=0&pitch=0&key=AIzaSyATLpwR01UbHlVaO1D0ahkSE5OsfKfpZd8";
        $url2{"$lat,$lon,$walk,$drive"} = "https://maps.googleapis.com/maps/api/streetview?size=640x300&fov=90&location=$lat,$lon&heading=240&pitch=0&key=AIzaSyATLpwR01UbHlVaO1D0ahkSE5OsfKfpZd8";
}
close(IN);

open(IN, "/home/enf/stackrank/asked2");
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

	if ($#k1 < 0) {
		@k1 = keys(%url);
		$k1 = $k1[rand($#k2)];
	}

	@k2 = keys(%url);
	$k2 = $k2[rand($#k2)];

	if (0) {
		if (! -s "/var/www/tlid/$k1.jpg") {
			system "curl -q -m60 -L -o /var/www/tlid/$k1.jpg '$url{$k1}'";
		}
	}

	if (! -s "/var/www/tlid/${k1}a.jpg") {
		system "curl -q -m60 -L -o /var/www/tlid/${k1}a.jpg '$url2{$k1}'";
	}
	($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size, $atime,$mtime,$ctime,$blksize,$blocks) = stat("/var/www/tlid/${k1}a.jpg");
	if ($size < 10000) {
		next;
	}

	if (0) {
		if (! -s "/var/www/tlid/$k2.jpg") {
			system "curl -q -m60 -L -o /var/www/tlid/$k2.jpg '$url{$k2}'";
		}
	}

	if (! -s "/var/www/tlid/${k2}a.jpg") {
		system "curl -q -m60 -L -o /var/www/tlid/${k2}a.jpg '$url2{$k2}'";
	}
	($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size, $atime,$mtime,$ctime,$blksize,$blocks) = stat("/var/www/tlid/${k2}a.jpg");
	if ($size < 10000) {
		next;
	}
	last;
}

print "<h1>Which one is more alive?</h1>\n";

print "<form action='/cgi-bin/ask2.cgi' method='post'>\n";
print "<input type='hidden' name='tlid1' value='$k1'>\n";
print "<input type='hidden' name='tlid2' value='$k2'>\n";

# print "<table><tr><td>";

print "<img src='/tlid/${k1}a.jpg'> ";
# print "<img src='/tlid/${k1}a.jpg'> ";
# print "<p>";
print "<input type='Submit' name='pref' value='First'>\n";
# print "</td><td>";
print "<p>\n";
print "<img src='/tlid/${k2}a.jpg'> ";
# print "<img src='/tlid/${k2}a.jpg'> ";
# print "<p>\n";
print "<input type='Submit' name='pref' value='Second'>\n";
# print "</td></tr>";

print "</form>\n";
