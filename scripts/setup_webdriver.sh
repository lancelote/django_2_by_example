wget "https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-$([[ $OSTYPE =~ darwin ]] && echo macos || echo linux).tar.gz"
mkdir -p vendor
tar -xzf geckodriver*.tar.gz -C vendor/
rm geckodriver*.tar.gz