"""
  Tashlin Reddy
  September 2020
  Version 1.0.0 
  Convert value and unit String in Base SI units
"""

import pint
import sys
import unit_parser
from pint import UnitRegistry
from astropy import units as u



class UnitConversion:
    def __init__(self, unit):
        
        ureg = UnitRegistry()
        self.unit = unit
        try:
            self.pint_unit = ureg(unit)
            print('pint unit')
        except pint.errors.UndefinedUnitError:
            try:
                parsed_unit = unit_parser.parse_string(str(self.unit))
                join_unit = ' * '.join(parsed_unit)
                self.pint_unit = ureg(join_unit)
                print('pint parse unit')
                
            except pint.errors.UndefinedUnitError:
                try:
                    astro_unit = self.unit.split(" ")
                    self.pint_unit = eval('(' + astro_unit[0] + '*' + 'u.'+ astro_unit[1] + ')')
                    print('astro unit')
                except:
                    print("Warning: Unit Not in Registry")
    
    def base_unit_conversion(self):
        try:
            base_unit = self.pint_unit.to_base_units()
            return base_unit

        except:
            try: 
                base_unit = self.pint_unit.si
                
            except:
                return self.unit

            else:
                return base_unit