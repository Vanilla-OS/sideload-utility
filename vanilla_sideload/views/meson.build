pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
viewsdir = join_paths(pkgdatadir, 'vanilla_sideload/views')

sources = [
  '__init__.py',
  'fail.py',
  'install_done.py',
  'install.py',
  'loading.py',
  'uninstall_done.py',
  'uninstall.py',
]

install_data(sources, install_dir: viewsdir)