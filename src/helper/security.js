// <script src="./security/forge/dist/forge.js"></script>

let pkeyBytes = fs.readFileSync('./public.pem');
let publicKey = forge.pki.publicKeyFromPem(pkeyBytes);

var encrypted = publicKey.encrypt(bytes, 'RSA-OAEP', {
    md: forge.md.sha256.create(),
    mgf1: {
      md: forge.md.sha1.create()
    }
});