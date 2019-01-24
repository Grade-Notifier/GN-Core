#!/bin/sh

# Python
while read p; do
pip3 install $p -U
done < ./Depfiles/dependencies.pip

# PHP
while read p; do
composer require p
done < ./Depfiles/dependencies.comp

# Node
if [[ "$OSTYPE" == "linux-gnu" ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash;
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install node;
    nvm use node;
fi

# CSS/Node
if [ "$HOSTNAME" = "venus" ] || [ "$HOSTNAME" = "mars" ] ; then
    npm install;
    gulp --gulpfile src/site/development-assets/generate-css.js;
fi

