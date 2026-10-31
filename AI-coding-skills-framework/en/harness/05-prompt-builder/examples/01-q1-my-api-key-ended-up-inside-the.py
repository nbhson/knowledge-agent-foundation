REDACT = [(re.compile(r'AKIA[0-9A-Z]{16}'), 'AWS_KEY'),
          (re.compile(r'ghp_[A-Za-z0-9]{36}'), 'GH_TOKEN'),
          (re.compile(r'-----BEGIN .*?PRIVATE KEY-----'), 'PRIVKEY')]
def delimit(text, source):
    esc = text.replace('</untrusted>', '<\\/untrusted>')
    return f'<untrusted source="{source}" len="{len(esc)}">{esc}</untrusted>'
