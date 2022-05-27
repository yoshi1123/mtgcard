# mtgcard - Command-line MTG card viewer and searcher.
# Copyright (C) 2020  yoshi1@tutanota.com
#
# mtgcard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mtgcard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mtgcard.  If not, see <https://www.gnu.org/licenses/>.

indexes = '''

create index cards_idx on cards(availability,name,printings,setCode,convertedManaCost,manaCost,power,toughness,loyalty,types,type,rarity,text,layout);
create index icard on cards(availability,name,setCode);
create index iprice on prices(uuid,price);
create index ilegal on legalities(uuid,format,status);
create index isets on sets(code, type desc, releaseDate desc);

'''.strip()
