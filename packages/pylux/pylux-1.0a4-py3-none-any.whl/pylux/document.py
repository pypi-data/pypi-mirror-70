# Pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
#
# Pylux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylux is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import decimal
import itertools
import json
import uuid
import math
from copy import deepcopy
from pylux.lib import constant, exception


# File operations. These functions load JSON documents from files and
# deserialise into strings which can be used by object retrieval functions.

def get_string_from_file(fp):
    '''Load a file into a string.'''

    with open(fp, 'r') as f:
        s = f.read()

    return s


def get_deserialised_document_from_string(s):
    '''Deserialise a JSON document into a list.'''

    return json.loads(s)


def write_to_file(doc, fp):
    '''Encode a document into a JSON file.'''

    with open(fp, 'w') as f:
        json.dump(doc, f)


# Object retrieval functions. These functions search a deserialised documents
# and return objects based on the given parameters.
def get_by_uuid(doc, uuid):
    '''Return object with given UUID.'''

    for obj in doc:
        if 'uuid' in obj:
            if obj['uuid'] == uuid:
                return obj


def get_by_key(doc, k):
    '''Return objects which have a key in their dict.'''

    matched = []

    for obj in doc:
        if k in obj:
            matched.append(obj)

    return matched


def get_by_value(doc, k, v):
    '''Return objects which have a key matching a value.'''

    matched = []

    for obj in get_by_key(doc, k):
        if str(obj[k]) == str(v):
            matched.append(obj)

    return matched


def get_by_type(doc, type):
    '''Return objects of a given type.'''

    return get_by_value(doc, 'type', type)


def get_by_ref(doc, type, ref):
    """Return an object of a given type and ref."""

    for obj in get_by_type(doc, type):
        if decimal.Decimal(obj['ref']).normalize() == decimal.Decimal(ref).normalize():
            return obj
    return False


def insert_blank_object(doc, obj_type, ref, **kwargs):
    """Insert a blank object of a type. Add the default blank object featuring only
    object type, ref and uuid. Then add any fields from the object type definition in
    lib.constant. If the values of any of these new keys were passed as kwargs to the
    insert_blank_object function, *and* are of the correct type (or can be converted
    to the correct type, then set the values of the keys to those kwargs passed. If
    no relevant kwarg was passed, just use the default value given in the object
    definition (usually an empty list, or dict)."""
    if str(ref) == '0':
        ref = autoref(doc, obj_type[0])
    new_obj = {
        'type': obj_type[0],
        'ref': str(ref),
        'uuid': str(uuid.uuid4())
    }
    for field, default_val in obj_type[2].items():
        if field in kwargs:
            if type(kwargs[field]) == type(field):
                new_obj[field] = kwargs[field]
            else:
                new_obj[field] = deepcopy(default_val)
        else:
            new_obj[field] = deepcopy(default_val)
    doc.append(new_obj)

    return new_obj


def insert_duplicate_object(doc, obj_type, src_obj, dest):
    """Copy an object to another, giving it a new UUID on the way."""
    dest_potential_clash = get_by_ref(doc, src_obj['type'], dest)
    if dest_potential_clash:
        raise exception.ObjectAlreadyExistsError(obj_type, dest)

    new_obj = deepcopy(src_obj)
    new_obj['ref'] = dest
    new_obj['uuid'] = str(uuid.uuid4())
    doc.append(new_obj)

    return new_obj


def get_metadata(doc):
    '''Return all metadata objects.'''

    return get_by_type(doc, 'metadata')


def remove_by_uuid(doc, uuid):
    '''Remove an object with a matching UUID.'''
    doc.remove(get_by_uuid(doc, uuid))


def remove_by_ref(doc, type, ref):
    """Remove an object with a specific ref."""
    doc.remove(get_by_ref(doc, type, ref))


def get_function_by_uuid(doc, uuid):
    '''Get a function by its UUID.'''

    for f in get_by_type(doc, 'fixture'):
        if 'personality' in f:
            for func in f['personality']:
                if func['uuid'] == uuid:
                    return func


def get_function_parent(doc, func):
    '''Get the associated fixture of a function.'''

    for f in get_by_type(doc, 'fixture'):
        if 'personality' in f:
            if func in f['personality']:
                return f


def get_occupied_addresses(reg):
    """Get a list of occupied addresses in a registry"""
    return sorted([int(d) for d in reg['table'].keys()])


def get_available_addresses(reg):
    """Get available addresses in a registry."""
    all = [i for i in range(1, 513)]
    occupied = get_occupied_addresses(reg)
    available = [i for i in all if i not in occupied]
    return sorted(available)


def get_start_address(reg, n):
    """Get start address in a registry given a required length."""
    available = get_available_addresses(reg)
    for addr in available:
        if set([i for i in range(addr, addr+n)]).issubset(available):
            return addr


def safe_address_fixture_by_ref(doc, fix_ref, univ, addr):
    """Register the functions of a fixture in a specified registry, beginning from a specified address. Register
        the functions in the order of their offset value. Alternatively, provide with address zero to
        pick an automatic starting address. Note that by default functions will overflow into the next registry if a
        registry is filled before all functions are registered. If registries with the specified references do not
        exist, new ones will be created. Registries are assumed to start at zero, in ArtNet style.
        Alternatively to providing a universe/address pair, give universe zero and any address to
        calculate the appropriate universe."""
    reg = get_by_ref(doc, 'registry', univ)
    while not reg:
        insert_blank_registry(doc, str(univ))
        reg = get_by_ref(doc, 'registry', univ)
    fixture = get_by_ref(doc, 'fixture', fix_ref)
    n = len(fixture['personality'])
    if n > 0:
        if addr == 0:
            addr = get_start_address(reg, n)
        for func in fixture['personality']:
            if addr > 512:
                univ += 1
                reg = get_by_ref(doc, 'registry', univ)
                while not reg:
                    insert_blank_registry(doc, univ)
                    reg = get_by_ref(doc, 'registry', univ)
                addr = addr % 512
            reg['table'][addr] = func['uuid']
            addr += 1


def unpatch_fixture_by_ref(doc, fix_ref):
    fix = get_by_ref(doc, 'fixture', fix_ref)
    func_ids = [func['uuid'] for func in fix['personality']]
    for reg in get_by_type(doc, 'registry'):
        for d in deepcopy(reg['table']):
            if reg['table'][d] in func_ids:
                del reg['table'][d]


def insert_duplicate_fixture_by_ref(doc, src_ref, dest_ref):
    dest = deepcopy(get_by_ref(doc, 'fixture', src_ref))
    dest['uuid'] = str(uuid.uuid4())
    dest['ref'] = dest_ref
    if 'personality' in dest:
        for func in dest['personality']:
            func['uuid'] = str(uuid.uuid4())
    doc.append(dest)


def fill_missing_function_uuids(fix):
    """Add new UUIDs to the functions of a fixture where they are missing."""
    if 'personality' in fix:
        for func in fix['personality']:
            if 'uuid' not in func:
                func['uuid'] = str(uuid.uuid4())


def find_fixture_intens(fix):
    if 'personality' in fix:
        for func in fix['personality']:
            if func['param'] == 'Dimmer':
                return func
    return None


def insert_blank_fixture(doc, ref):
    return insert_blank_object(doc, constant.FIXTURE_TYPE, ref)


def insert_fixture_from_json_template(doc, ref, template_file):
    fixture = insert_blank_fixture(doc, ref)
    with open(template_file) as f:
        template = json.load(f)
        for k, v in template.items():
            fixture[k] = v
    if 'personality' in fixture:
        for function in fixture['personality']:
            function['uuid'] = str(uuid.uuid4())


def complete_fixture_from_json_template(fix, template_file):
    with open(template_file) as f:
        template = json.load(f)
        if 'personality' in template and 'personality' not in fix:
            fix['personality'] = template['personality']
            for func in fix['personality']:
                func['uuid'] = str(uuid.uuid4())
        for k in template:
            if k not in fix:
                fix[k] = template[k]


def update_fixture_from_json_template(fix, template_file):
    with open(template_file) as f:
        template = json.load(f)
        for k, v in template.items():
            if k != 'personality':
                fix[k] = v


def insert_blank_group(doc, ref):
    return insert_blank_object(doc, constant.GROUP_TYPE, ref)


def group_append_fixture_by_ref(doc, group, fix_ref):
    fix = get_by_ref(doc, 'fixture', fix_ref)
    if fix:
        group['fixtures'].append(fix['uuid'])


def insert_blank_registry(doc, ref):
    registry = {
        'type': 'registry',
        'ref': str(ref),
        'uuid': str(uuid.uuid4()),
        'table': {}

    }
    doc.append(registry)
    return registry


def insert_blank_cue(doc, ref):
    return insert_blank_object(doc, constant.CUE_TYPE, ref)


def set_cue_fixture_level(cue, fix, level):
    """Set the level of a fixture in a cue. Automatically decides on the function by finding the
    Intens function."""
    intens = find_fixture_intens(fix)
    cue['levels'][intens['uuid']] = level


def set_cue_fixture_level_by_fixture_ref(doc, cue, fix_ref, level):
    """Set cue fixture level as in set_cue_fixture_level, except accept a fixture reference rather than
    fixture object."""
    fix = get_by_ref(doc, 'fixture', fix_ref)
    set_cue_fixture_level(cue, fix, level)


def set_cue_function_level(doc, cue, func, level):
    """Set the level of a function, in a cue."""
    fix = get_function_parent(doc, func)
    # Check to see if the function is a 16 bit function by checking for
    # functions with the (16b) suffix with the same name
    fine_func = get_by_value(fix['personality'], 'param', func['param'] + ' (16b)')
    if fine_func:
        # Logic to determine 16bit values
        try:
            upper_bit = math.floor(int(level) / 256)
            lower_bit = int(level) % 256
        except ValueError:
            upper_bit = level
            lower_bit = level
        cue['levels'][func['uuid']] = str(upper_bit)
        cue['levels'][fine_func[0]['uuid']] = str(lower_bit)
    else:
        cue['levels'][func['uuid']] = level


def insert_blank_intensity_palette(doc, ref):
    return insert_blank_object(doc, constant.INTENSITY_PALETTE_TYPE, ref)


def insert_blank_focus_palette(doc, ref):
    return insert_blank_object(doc, constant.FOCUS_PALETTE_TYPE, ref)


def insert_blank_colour_palette(doc, ref):
    return insert_blank_object(doc, constant.COLOUR_PALETTE_TYPE, ref)


def insert_blank_beam_palette(doc, ref):
    return insert_blank_object(doc, constant.BEAM_PALETTE_TYPE, ref)


def insert_blank_all_palette(doc, ref):
    return insert_blank_object(doc, constant.ALL_PALETTE_TYPE, ref)


def set_palette_function_level(doc, palette, func, level):
    """Set the level of a function, in a palette."""
    fix = get_function_parent(doc, func)
    # Check to see if the function is a 16 bit function by checking for
    # functions with the (16b) suffix with the same name
    fine_func = get_by_value(fix['personality'], 'param', func['param'] + ' (16b)')
    if fine_func:
        # Logic to determine 16bit values
        try:
            upper_bit = math.floor(int(level) / 256)
            lower_bit = int(level) % 256
        except ValueError:
            upper_bit = level
            lower_bit = level
        palette['levels'][func['uuid']] = str(upper_bit)
        palette['levels'][fine_func[0]['uuid']] = str(lower_bit)
    else:
        palette['levels'][func['uuid']] = level


def get_function_patch_location(doc, func):
    """Finds a function in all registries and returns registry, address tuple."""
    locations = []
    for reg in get_by_type(doc, 'registry'):
        for d in reg['table']:
            if reg['table'][d] == func['uuid']:
                return reg['ref'], d


def insert_filter_with_params(doc, ref, k, v):
    """Create a new filter with the given parameters."""
    return insert_blank_object(doc, constant.FILTER_TYPE, ref, k=k, v=v)


def autoref(doc, type):
    """Return an available reference number for a given type."""
    used_refs = []
    for obj in get_by_type(doc, type):
        used_refs.append(obj['ref'])

    for n in itertools.count(start=1):
        if str(n) not in used_refs:
            return str(n)


def create_parent_metadata_object(doc):
    doc.append(
        {'type': 'metadata',
         'tags': {}}
    )


def parent_metadata_object_exists(doc):
    if len(get_by_type(doc, 'metadata')) > 0:
        return True
    else:
        return False


def get_parent_metadata_object(doc):
    try:
        metadata = get_by_type(doc, 'metadata')[0]
    except IndexError:
        create_parent_metadata_object(doc)
        metadata = get_by_type(doc, 'metadata')[0]
    finally:
        return metadata


def remove_metadata(doc, k):
    if parent_metadata_object_exists(doc):
        obj = get_parent_metadata_object(doc)
        if k in obj['tags']:
            del obj['tags'][k]


def set_metadata(doc, k, v):
    """Set metadata value"""
    if not parent_metadata_object_exists(doc):
        create_parent_metadata_object(doc)
    get_parent_metadata_object(doc)['tags'][k] = v


def get_metadata(doc, k):
    """Get a metadata value if it exists, else return None"""
    if not parent_metadata_object_exists(doc):
        return None
    metadata_object = get_parent_metadata_object(doc)
    if k not in metadata_object['tags']:
        return None
    else:
        return metadata_object['tags'][k]
