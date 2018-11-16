version="v0.23.0"
os="$([[ $OSTYPE =~ darwin ]] && echo macos || echo linux64)"

wget "https://github.com/mozilla/geckodriver/releases/download/${version}/geckodriver-${version}-${os}.tar.gz"
mkdir -p vendor
tar -xzf geckodriver*.tar.gz -C vendor/
rm geckodriver*.tar.gz