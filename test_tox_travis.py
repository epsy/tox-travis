import os
import subprocess


tox_ini = b"""
[tox]
envlist = py26, py27, py32, py33, py34, pypy, pypy3, docs
"""

tox_ini_override = tox_ini + b"""
[tox:travis]
2.7 = py27, docs
"""

tox_ini_factors = b"""
[tox]
envlist = py34, py34-docs, py34-django, dontmatch-1
"""

tox_ini_factors_override = tox_ini_factors + b"""
[tox:travis]
2.7 = py27-django
"""

tox_ini_factors_override_nonenvlist = tox_ini_factors + b"""
[tox:travis]
3.4 = py34, extra

[testenv:extra-coveralls]
basepython=python3.4

[testenv:extra-flake8]
basepython=python3.4

[testenv:dontmatch-2]
basepython=python3.4
"""

tox_ini_django_factors = b"""
[tox]
envlist = py{27,34}-django, other

[tox:travis]
2.7 = django
3.4 = other
"""


class TestToxTravis:
    def tox_envs(self):
        """Find the envs that tox sees."""
        output = subprocess.Popen(
            ['tox', '-l'], stdout=subprocess.PIPE).communicate()[0]
        return output.decode('utf-8').strip().split()

    def test_not_travis(self, tmpdir):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini)

        expected = [
            'py26', 'py27', 'py32', 'py33', 'py34',
            'pypy', 'pypy3', 'docs',
        ]

        assert self.tox_envs() == expected

    def test_travis_default_26(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '2.6')

        assert self.tox_envs() == ['py26']

    def test_travis_default_27(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '2.7')

        assert self.tox_envs() == ['py27']

    def test_travis_default_32(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '3.2')

        assert self.tox_envs() == ['py32']

    def test_travis_default_33(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '3.3')

        assert self.tox_envs() == ['py33']

    def test_travis_default_34(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '3.4')

        assert self.tox_envs() == ['py34']

    def test_travis_default_pypy(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', 'pypy')

        assert self.tox_envs() == ['pypy']

    def test_travis_default_pypy3(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', 'pypy3')

        assert self.tox_envs() == ['pypy3']

    def test_travis_override(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini_override)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '2.7')

        assert self.tox_envs() == ['py27', 'docs']

    def test_respect_overridden_toxenv(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '2.7')
        monkeypatch.setenv('TOXENV', 'py32')

        assert self.tox_envs() == ['py32']

    def test_keep_if_no_match(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini_factors)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '2.7')

        assert self.tox_envs() == ['py27']

    def test_default_tox_ini_overrides(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini_factors_override)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '2.7')

        assert self.tox_envs() == ['py27-django']

    def test_factors(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini_factors)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '3.4')

        assert self.tox_envs() == ['py34', 'py34-docs', 'py34-django']

    def test_match_and_keep(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini_factors_override_nonenvlist)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '3.4')

        assert self.tox_envs() == ['py34', 'py34-docs', 'py34-django',
                                   'extra-coveralls', 'extra-flake8']

    def test_django_factors(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini_django_factors)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '2.7')

        assert self.tox_envs() == ['py27-django', 'py34-django']

    def test_non_python_factor(self, tmpdir, monkeypatch):
        os.chdir(str(tmpdir))
        tmpdir.join('tox.ini').write(tox_ini_django_factors)

        monkeypatch.setenv('TRAVIS', 'true')
        monkeypatch.setenv('TRAVIS_PYTHON_VERSION', '3.4')

        assert self.tox_envs() == ['other']
