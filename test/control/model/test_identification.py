import os

import pytest
import where
from pysystem import SystemUser, SystemGroup

from pji.control import Identification


@pytest.mark.unittest
class TestControlModelIdentification:
    def test_properties(self):
        ident = Identification('nobody', 'nogroup')
        assert ident.user.name == 'nobody'
        assert ident.group.name == 'nogroup'

        ident = Identification('root', 'root')
        assert ident.user.name == 'root'
        assert ident.group.name == 'root'

    def test_current(self):
        ci = Identification.current()
        assert ci.user == SystemUser.current()
        assert ci.group == SystemGroup.current()

    def test_load_from_file(self):
        _sh_file = where.first('sh')
        fi = Identification.load_from_file(_sh_file)
        assert fi.user == SystemUser.load_from_file(_sh_file)
        assert fi.group == SystemGroup.load_from_file(_sh_file)

    def test_init(self):
        ident = Identification('nobody')
        assert ident.user.name == 'nobody'
        assert ident.group is None

        ident = Identification('nobody', auto_group=True)
        assert ident.user.name == 'nobody'
        assert ident.group.name == 'nogroup'

        ident = Identification(None, 'nogroup')
        assert ident.user is None
        assert ident.group.name == 'nogroup'

    def test_to_json(self):
        assert Identification('nobody', 'nogroup').to_json() == {'user': 'nobody', 'group': 'nogroup'}
        assert Identification('nobody', None).to_json() == {'user': 'nobody', 'group': None}
        assert Identification(None, 'nogroup').to_json() == {'user': None, 'group': 'nogroup'}
        assert Identification(None, None).to_json() == {'user': None, 'group': None}

    def test_eq(self):
        ident = Identification('nobody', 'nogroup')
        assert ident == ident
        assert not (ident == 1)

        assert Identification('nobody', 'nogroup') == Identification.loads({'user': 'nobody', 'group': 'nogroup'})
        assert Identification('nobody') == Identification.loads({'user': 'nobody'})
        assert Identification('root', 'root') == Identification.loads({'user': 'root', 'group': 'root'})

    def test_eq_and_hash(self):
        d = {
            Identification('nobody', 'nogroup'): 1,
            Identification('nobody'): 2,
            Identification('root', 'root'): 3,
        }

        assert d[Identification.loads({'user': 'nobody', 'group': 'nogroup'})] == 1
        assert d[Identification.loads({'user': 'nobody'})] == 2
        assert d[Identification.loads({'user': 'root', 'group': 'root'})] == 3

    def test_loads(self):
        ident = Identification('nobody', 'nogroup')
        assert Identification.loads(ident) == ident
        assert Identification.loads({'user': 'nobody', 'group': 'nogroup'}) == ident
        assert Identification.loads(('nobody', 'nogroup')) == ident
        assert Identification.loads(SystemUser.loads('nobody')) == ident
        assert Identification.loads(SystemGroup.loads('nogroup')) == Identification(None, 'nogroup')
        assert Identification.loads('nobody') == ident
        with pytest.raises(ValueError):
            Identification.loads('nogroup')

    def test_merge(self):
        assert Identification.merge() == Identification()
        assert Identification.merge('root') == Identification('root', 'root')
        assert Identification.merge(('nobody', 'nogroup'), 'root') == Identification('root', 'root')
        assert Identification.merge('root', 'nobody', ('root', None)) == Identification('root', 'nogroup')

    def test_repr(self):
        assert repr(Identification('nobody', 'nogroup')) == '<Identification user: nobody, group: nogroup>'
        assert repr(Identification('nobody')) == '<Identification user: nobody>'
        assert repr(Identification(None, 'nogroup')) == '<Identification group: nogroup>'
        assert repr(Identification()) == '<Identification>'


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
