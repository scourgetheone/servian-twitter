#!/bin/bash
#
# build.sh: This script builds the frontend reactjs application and
# makes it available to the Flask web server.
#

# Remove previous react app bundles
rm -r static/app.js
rm -r static/app.*.js

# Bundle the react app in production mode.
pushd ui/ >/dev/null
webpack --mode production
popd >/dev/null

# Hash the file to prevent browser caching
hash=$(sha256sum static/app.js | head -c16)

# Create the index.html file if not exist
if [ ! -f /tmp/foo.txt ]; then
    cat > templates/index.html <<EOF
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Servian Real-time Tweet Stream</title>
    </head>
    <body>
        <div id="container"></div>
    </body>
    <script type="text/javascript" src="{{url_for('static', filename='app.123.js')}}"></script></body>
</html>
EOF
fi

# Rename the bundled react app file using the hash
mv static/app.js static/app.$hash.js

# update the hash to the react app's script path in index.html
sed -i "s/app[.0-9a-f]*\.js/app.$hash.js/" templates/index.html