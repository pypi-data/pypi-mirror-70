# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
# created 2019-02-15
import pytest
import ezdxf

from ezdxf.entities.insert import Insert
from ezdxf.lldxf.const import DXF12, DXF2000
from ezdxf.lldxf.tagwriter import TagCollector, basic_tags_from_text
from ezdxf.math import Vector

TEST_CLASS = Insert
TEST_TYPE = 'INSERT'

ENTITY_R12 = """0
INSERT
5
0
8
0
2
BLOCKNAME
10
0.0
20
0.0
30
0.0
41
1.0
42
1.0
43
1.0
50
0.0
"""

ENTITY_R2000 = """0
INSERT
5
0
330
0
100
AcDbEntity
8
0
100
AcDbBlockReference
2
BLOCKNAME
10
0.0
20
0.0
30
0.0
41
1.0
42
1.0
43
1.0
50
0.0
"""


@pytest.fixture(scope='module')
def doc():
    return ezdxf.new()


@pytest.fixture(params=[ENTITY_R12, ENTITY_R2000])
def entity(request):
    return TEST_CLASS.from_text(request.param)


def test_registered():
    from ezdxf.entities.factory import ENTITY_CLASSES
    assert TEST_TYPE in ENTITY_CLASSES


def test_default_init():
    entity = TEST_CLASS()
    assert entity.dxftype() == TEST_TYPE


def test_default_new():
    entity = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={
        'color': '7',
        'insert': (1, 2, 3),
    })
    assert entity.dxf.layer == '0'
    assert entity.dxf.color == 7
    assert entity.dxf.linetype == 'BYLAYER'
    assert entity.dxf.insert == (1, 2, 3)
    assert entity.dxf.insert.x == 1, 'is not Vector compatible'
    assert entity.dxf.insert.y == 2, 'is not Vector compatible'
    assert entity.dxf.insert.z == 3, 'is not Vector compatible'
    assert entity.has_scaling is False
    assert entity.has_uniform_scaling is True
    # can set DXF R2007 value
    entity.dxf.shadow_mode = 1
    assert entity.dxf.shadow_mode == 1


def test_has_scaling():
    entity = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={'xscale': 2})
    assert entity.has_scaling is True
    assert entity.has_uniform_scaling is False
    entity = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={'yscale': 2})
    assert entity.has_scaling is True
    assert entity.has_uniform_scaling is False
    entity = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={'zscale': 2})
    assert entity.has_scaling is True
    assert entity.has_uniform_scaling is False
    entity = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={
        'xscale': -2,  # mirroring has the same problems like non uniform scaling
        'yscale': 2,
        'zscale': 2,
    })
    assert entity.has_uniform_scaling is False


def test_load_from_text(entity):
    assert entity.dxf.layer == '0'
    assert entity.dxf.color == 256, 'default color is 256 (by layer)'
    assert entity.dxf.insert == (0, 0, 0)
    assert entity.has_scaling is False


@pytest.mark.parametrize("txt,ver", [(ENTITY_R2000, DXF2000), (ENTITY_R12, DXF12)])
def test_write_dxf(txt, ver):
    expected = basic_tags_from_text(txt)
    vertex = TEST_CLASS.from_text(txt)
    collector = TagCollector(dxfversion=ver, optional=True)
    vertex.export_dxf(collector)
    assert collector.tags == expected

    collector2 = TagCollector(dxfversion=ver, optional=False)
    vertex.export_dxf(collector2)
    assert collector.has_all_tags(collector2)


def test_add_attribs(doc):
    insert = Insert(doc)
    assert insert.attribs_follow is False
    insert.add_attrib('T1', 'value1', (0, 0))
    assert len(insert.attribs) == 1
    assert insert.attribs_follow is True


def test_get_block(doc):
    blk = doc.blocks.new('TEST-2020-02-29')
    msp = doc.modelspace()
    insert = msp.add_blockref('TEST-2020-02-29', (0, 0))
    assert insert.block() is blk
    insert = msp.add_blockref('NOT-EXIST-2020-02-29', (0, 0))
    assert insert.block() is None
    insert = Insert()
    assert insert.block() is None


def test_clone_with_insert(doc):
    # difference of clone() to copy_entity() is:
    # - clone returns and unassigned entity without handle, owner or reactors
    # - copy_entity clones the entity and assigns the new entity to the same owner as the source and adds the entity
    #   and it linked entities (ATTRIB & VERTEX) to the entity database, but does not adding entity to a layout, setting
    #   owner tag is not enough to assign an entity to a layout, use Layout.add_entity()
    insert = doc.dxffactory.create_db_entry('INSERT', dxfattribs={})
    insert.add_attrib('T1', 'value1', (0, 0))
    clone = insert.copy()
    assert clone.dxf.handle is None
    assert clone.dxf.owner is None
    assert len(clone.attribs) == 1
    attrib = clone.attribs[0]
    assert attrib.dxf.handle is None
    assert attrib.dxf.tag == 'T1'
    assert attrib.dxf.text == 'value1'
    # change cloned attrib
    attrib.dxf.tag = 'T2'
    attrib.dxf.text = 'value2'
    # source attrib is unchanged
    assert insert.attribs[0].dxf.tag == 'T1'
    assert insert.attribs[0].dxf.text == 'value1'


def test_copy_with_insert(doc):
    msp = doc.modelspace()
    msp_count = len(msp)
    db_count = len(doc.entitydb)

    insert = msp.add_blockref('Test', insert=(0, 0))
    assert insert.seqend.dxf.owner == insert.dxf.owner
    assert insert.seqend.dxf.handle is not None
    assert insert.seqend.dxf.handle in doc.entitydb

    insert.add_attrib('T1', 'value1')

    # linked attribs not stored in the entity space
    assert len(msp) == msp_count + 1
    # attribs stored in the entity database + SEQEND
    assert len(doc.entitydb) == db_count + 3

    copy = doc.entitydb.duplicate_entity(insert)

    # not duplicated in entity space
    assert len(msp) == msp_count + 1
    # duplicated in entity database (2x SEQEND)
    assert len(doc.entitydb) == db_count + 6

    # get 1. paperspace in tab order
    psp = doc.layout()
    psp.add_entity(copy)
    assert len(psp) == 1

    assert copy.dxf.handle is not None
    assert copy.dxf.handle != insert.dxf.handle
    assert copy.dxf.owner == psp.layout_key
    assert copy.attribs[0].dxf.owner == psp.layout_key


def test_brcs_no_transform():
    insert = TEST_CLASS.new(handle='ABBA', owner='0')
    brcs = insert.brcs()
    assert brcs.to_wcs((0, 0, 0)) == (0, 0, 0)
    assert brcs.direction_to_wcs((1, 0, 0)) == (1, 0, 0)


def test_brcs_insert():
    insert = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={
        'insert': (1, 2, 3),
    })
    brcs = insert.brcs()
    assert brcs.to_wcs((0, 0, 0)) == (1, 2, 3)
    assert brcs.direction_to_wcs((1, 0, 0)) == (1, 0, 0)


def test_brcs_insert_and_base_point(doc):
    doc.blocks.new('BRCS_001', base_point=(2, 2, 2))
    insert = doc.modelspace().add_blockref('BRCS_001', insert=(1, 2, 3))
    brcs = insert.brcs()
    assert brcs.to_wcs((0, 0, 0)) == (-1, 0, 1)
    assert brcs.direction_to_wcs((1, 0, 0)) == (1, 0, 0)


def test_brcs_rotation():
    insert = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={
        'insert': (0, 0, 0),
        'rotation': 90,
    })
    brcs = insert.brcs()
    assert list(brcs.points_to_wcs([(1, 0, 0), (0, 0, 1)])) == [(0, 1, 0), (0, 0, 1)]
    assert brcs.direction_to_wcs((1, 0, 0)) == (0, 1, 0)


def test_brcs_scaled():
    insert = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={
        'xscale': 2,
        'yscale': 3,
        'zscale': 4,
    })
    brcs = insert.brcs()
    assert brcs.to_wcs((1, 1, 1)) == (2, 3, 4)
    assert brcs.direction_to_wcs((1, 0, 0)) == (2, 0, 0), 'scaling has to be applied for directions'


def test_brcs_dircection():
    insert = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={
        'insert': (1, 2, 3),
        'xscale': 2,
    })
    brcs = insert.brcs()
    assert brcs.to_wcs((1, 0, 0)) == (3, 2, 3)
    assert brcs.direction_to_wcs((1, 0, 0)) == (2, 0, 0), 'only scaling has to be applied for directions'
