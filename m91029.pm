#!/usr/bin/env perl

##
## Author......: See docs/credits.txt
## License.....: MIT
##

use strict;
use warnings;

use Encode qw (encode);
use MIME::Base64;
use Digest::SHA qw (sha256);

sub module_constraints { [[0, 256], [-1, -1], [0, 55], [-1, -1], [-1, -1]] }

sub module_generate_hash
{
  my $word = shift;

  my $digest = encode_base64(sha256(encode("UTF-16le", $word)), ''); # encode_base64 defaults to adding a newline, https://www.perlmonks.org/?node_id=660422

  my $hash = sprintf ("%s", $digest);

  return $hash;
}

sub module_verify_hash
{
  my $line = shift;


  my ($hash, $word) = split (':', $line);

  return unless defined $hash;
  return unless defined $word;

  my $word_packed = pack_if_HEX_notation ($word);

  my $new_hash = module_generate_hash ($word_packed);

  return ($new_hash, $word);
}

1;
