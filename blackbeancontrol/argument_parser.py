import argparse
import sys

from .utils import pprint

class ArgumentParser:
  def __init__(self):
  
    self._parser = argparse.ArgumentParser()
    
    subparsers = self._parser.add_subparsers(
      title = 'sub-commands',
      description = 'available commands',
      dest = 'subparser_name',
      help = 'action to be performed by the script'
    )
    
    command_parser = subparsers.add_parser(
      'command',
      help='learn or send an IR command'
    )
    
    command_parser.add_argument(
      'command',
      nargs='+',
      type=str,
      help='commands which should be learned/sent'
    )
    
    command_parser.add_argument(
      '-d',
      '--device',
      type=str,
      default='',
      help='name of the device to use'
    )
    
    command_parser.add_argument(
      '-i',
      '--ipaddress',
      type=str,
      default='',
      help='ip address of the device which should be used'
    )
    
    command_parser.add_argument(
      '-p',
      '--port',
      type=int,
      default=80,
      help='port to use when connecting to the device'
    )
    
    command_parser.add_argument(
      '-m',
      '--mac',
      type=str,
      default='',
      help='mac address of the device'
    )
    
    command_parser.add_argument(
      '-y',
      '--type',
      type=str,
      default='',
      help='device type (see either discovery results or python-broadlink package)'
    )

    command_parser.add_argument(
      '-t',
      '--timeout',
      type=int,
      default=10,
      help='timeout for device actions'
    )

    command_parser.add_argument(
      '-e',
      '--repeat',
      type=int,
      default=1,
      help='repeat sending the given commands a given number of times'
    )

    discovery_parser = subparsers.add_parser(
      'discover',
      help='discover all supported devices in your local network'
    )

    discovery_parser.add_argument(
      'timeout',
      type=int,
      default=10,
      help='timeout when waiting for available devices to show up'
    )

  def run(self):
  
    result = self._parser.parse_args()
    
    res = {
      'mode': '',
      'commands': [],
      'device': '',
      'ipaddress': '',
      'mac': '',
      'port': -1,
      'timeout': -1,
      'type': '',
      'repeat': 1,
    }

    if result.subparser_name == 'command':
      res['mode'] = 'command'
      
      res['commands'] = result.command[:]
      res['repeat'] = result.repeat

      if result.device.strip():
        res['device'] = result.device.strip()
      
        if result.type.strip() or result.ipaddress.strip() or result.mac.strip():
          pprint('You can only provide either a device name from the ' +
                 'configuration file or host, mac, type and additional parameters of a device'
          )
        
          sys.exit(2)
        
      elif not result.mac.strip() and not result.type.strip() and not result.ipaddress.strip():
      
        res['device'] = 'General'

      else:
      
        if not result.type.strip() or not result.ipaddress.strip() or not result.mac.strip():
          pprint('you need to provide either a device name from the ' + 
                 'configuration file or host, mac address, type and additional parameters of a ' + 
                 'device'
          )
          
          sys.exit(2)
        
        res['ipaddress'] = result.ipaddress.strip()
        res['mac'] = result.mac.strip()
        res['port'] = result.port
        res['timeout'] = result.timeout
        res['type'] = result.type.strip()
      
      for i, cmd in enumerate(res['commands']):
      
        try:
          res['commands'][i] = int(cmd)
        except ValueError:
          continue

    elif result.subparser_name == 'discover':
      
      res['mode'] = 'discover'
      res['timeout'] = result.timeout

    else:
      result = self._parser.parse_args(('--help', ))
      sys.exit(2)

    return res