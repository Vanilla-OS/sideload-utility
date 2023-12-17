pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
backenddir = join_paths(pkgdatadir, 'vanilla_sideload/backend')

sources = [
  '__init__.py',
  'dpkg.py',
  'types.py',
  'utils.py',
  'run_async.py',
]

install_data(sources, install_dir: backenddir)