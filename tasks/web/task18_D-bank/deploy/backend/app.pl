use Mojolicious::Lite;
use Crypt::DES;
use Digest::MD5 qw(md5_hex);
use Digest::SHA qw(sha256_hex);
use MIME::Base64;
use Crypt::JWT qw(encode_jwt decode_jwt);
use Crypt::PRNG qw(random_bytes);
use Time::HiRes qw(time);

my $secret_key = random_bytes(8);
my $jwt_secret = encode_base64(random_bytes(32), '');

# In-memory storage for simplicity
my %users;

my $flag = $ENV{FLAG};

sub generate_wallet_address {
    my ($username, $email) = @_;
    return sha256_hex($username . $email);
}

sub generate_signature {
    my ($message) = @_;
    my $md5_hash = md5_hex($message);
    my $des = Crypt::DES->new($secret_key);
    my $encrypted_hash = $des->encrypt('00'.substr($md5_hash, 0, 6));
    return encode_base64($encrypted_hash, '');
}

sub verify_signature {
    my ($message, $provided_signature) = @_;
    my $md5_hash = md5_hex($message);
    my $des = Crypt::DES->new($secret_key);
    my $encrypted_hash = decode_base64($provided_signature);
    my $decrypted_hash = $des->decrypt($encrypted_hash);
    return '00'.substr($md5_hash, 0, 6) eq $decrypted_hash;
}

# Register a new user and generate their wallet address
post '/register' => sub {
    my $c = shift;
    
    # Parse the JSON data from the request body
    my $json = $c->req->json;
    my $username = $json->{username};
    my $email = $json->{email};
    my $password = $json->{password};

    unless ($username && $email && $password) {
        return $c->render(json => { error => "Missing parameters" }, status => 400);
    }

    if (exists $users{$username}) {
        return $c->render(json => { error => "User already exists" }, status => 400);
    }

    my $wallet_address = generate_wallet_address($username, $email);
    $users{$username} = { email => $email, wallet_address => $wallet_address, password => $password, balance => 10 };

    $c->render(json => { wallet_address => $wallet_address });
};

# Login user and return JWT token
post '/login' => sub {
    my $c = shift;
    my $json = $c->req->json;
    my $username = $json->{username};
    my $password = $json->{password};

    unless ($username && $password) {
        return $c->render(json => { error => "Missing parameters" }, status => 400);
    }

    if (!exists $users{$username}) {
        return $c->render(json => { error => "User not found" }, status => 400);
    }

    if ($users{$username}->{password} ne $password) {
        return $c->render(json => { error => "Incorrect password" }, status => 400);
    }

    my $token = encode_jwt(payload => { username => $username }, key => $jwt_secret, alg => 'HS256');

    $c->render(json => { token => $token, wallet_address => $users{$username}->{wallet_address} });
};

# Return balance of logged user
post '/balance' => sub {
    my $c = shift;

    my $token = $c->req->headers->header('Authorization');
    $token =~ s/^Bearer\s+// if $token;

    my $decoded;
    eval {
        $decoded = decode_jwt(token => $token, key => $jwt_secret, alg => 'HS256');
    };
    if ($@ || !$decoded || !$decoded->{username}) {
        return $c->render(json => { error => "Unauthorized" }, status => 401);
    }

    my $username = $decoded->{username};
    my $balance = $users{$username}->{balance};

    $c->render(json => { balance => $balance });
};

# Create a stateless package (JWT) for a specific wallet address
post '/create-package' => sub {
    my $c = shift;
    my $json = $c->req->json;

    my $token = $c->req->headers->header('Authorization');
    $token =~ s/^Bearer\s+// if $token;

    my $decoded;
    eval {
        $decoded = decode_jwt(token => $token, key => $jwt_secret, alg => 'HS256');
    };
    if ($@ || !$decoded || !$decoded->{username}) {
        return $c->render(json => { error => "Unauthorized" }, status => 401);
    }

    my $username = $decoded->{username};
    my $recipient_address = $json->{recipientAddress};
    my $amount = $json->{amount};

    unless ($recipient_address && $amount) {
        return $c->render(json => { error => "Missing parameters" }, status => 400);
    }

    if ($users{$username}->{balance} < $amount) {
        return $c->render(json => { error => "Insufficient funds" }, status => 400);
    }

    if ($recipient_address eq "1337133713371337133713371337133713371337133713371337133713371337") {
        return $c->render(json => { error => "Антифрод система заблокировала операцию"}, status => 418);
    }

    my $package_data = {
        sender => $users{$username}->{wallet_address},
        recipient => $recipient_address,
        amount => $amount,
        timestamp => time
    };

    my $message = join('|', @$package_data{qw(sender recipient amount timestamp)});
    my $signature = generate_signature($message);

    my $package = encode_jwt(
        payload => {
            %$package_data,
            signature => $signature
        },
        key => $jwt_secret,
        alg => 'none',
        allow_none => 1
    );

    $users{$username}->{balance} -= $amount;

    $c->render(json => { handoff => $package });
};

post '/redeem-package' => sub {
    my $c = shift;
    my $json = $c->req->json;

    my $token = $c->req->headers->header('Authorization');
    $token =~ s/^Bearer\s+// if $token;

    my $decoded;
    eval {
        $decoded = decode_jwt(token => $token, key => $jwt_secret, alg => 'HS256');
    };
    if ($@ || !$decoded || !$decoded->{username}) {
        return $c->render(json => { error => "Unauthorized" }, status => 401);
    }

    my $username = $decoded->{username};
    my $package = $json->{handoff};

    unless ($package) {
        return $c->render(json => { error => "Missing package" }, status => 400);
    }

    my $package_data;
    eval {
        $package_data = decode_jwt(token => $package, key => $jwt_secret, alg => 'none', allow_none => 1);
    };
    if ($@ || !$package_data) {
        return $c->render(json => { error => "Invalid package" }, status => 400);
    }

    unless (verify_signature(
        join('|', @$package_data{qw(sender recipient amount timestamp)}),
        $package_data->{signature}
    )) {
        return $c->render(json => { error => "Invalid signature" }, status => 400);
    }

    if ($package_data->{recipient} ne $users{$username}->{wallet_address}) {
        return $c->render(json => { error => "This package is not for your wallet address" }, status => 400);
    }

    $users{$username}->{balance} += $package_data->{amount};

    $c->render(json => { success => 1, balance => $users{$username}->{balance} });
};

post '/get-flag' => sub {
    my $c = shift;
    my $json = $c->req->json;

    my $token = $c->req->headers->header('Authorization');
    $token =~ s/^Bearer\s+// if $token;

    my $decoded;
    eval {
        $decoded = decode_jwt(token => $token, key => $jwt_secret, alg => 'HS256');
    };
    if ($@ || !$decoded || !$decoded->{username}) {
        return $c->render(json => { error => "Unauthorized" }, status => 401);
    }

    my $username = $decoded->{username};
    my $package = $json->{handoff};

    unless ($package) {
        return $c->render(json => { error => "Missing package" }, status => 400);
    }

    my $package_data;
    eval {
        $package_data = decode_jwt(token => $package, key => $jwt_secret, alg => 'none', allow_none => 1);
    };
    if ($@ || !$package_data) {
        return $c->render(json => { error => "Invalid package" }, status => 400);
    }

    unless (verify_signature(
        join('|', @$package_data{qw(sender recipient amount timestamp)}),
        $package_data->{signature}
    )) {
        return $c->render(json => { error => "Invalid signature" }, status => 400);
    }
    if ($package_data->{recipient} ne "1337133713371337133713371337133713371337133713371337133713371337") {
        return $c->render(json => { error => "This package is not for flag wallet address" }, status => 400);
    }
    if ($package_data->{amount} ne "133713371337") {
        return $c->render(json => { error => "This package contains not enough money" }, status => 400);
    }

    return $c->render(json => { success => 1, flag => $flag })
};

app->start;