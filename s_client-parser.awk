#!/usr/bin/awk -f

# Match all certificates
/^-----BEGIN CERTIFICATE-----$/ { in_cert=1; }
in_cert { cert = cert $0 "\n"; }
/^-----END CERTIFICATE-----$/ { in_cert = 0; }
!in_cert && cert {
    #infocmd="openssl x509 -text -noout | grep -E 'Public-Key:|Subject:'";
    infocmd="openssl x509 -text -noout";
    print cert | infocmd;
    close(infocmd);
    cert="";
}
# Print the verification result
/Verify return code/
