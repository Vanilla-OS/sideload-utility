application_id = 'org.vanillaos.Sideload'


scalable_dir = join_paths('hicolor', 'scalable', 'apps')
symbolic_dir = join_paths('hicolor', 'symbolic')
actions_dir = join_paths(symbolic_dir, 'actions')


install_data(
  join_paths(scalable_dir, ('@0@.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir)
)


install_data(
  join_paths(symbolic_dir, 'apps', ('@0@-symbolic.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir, 'apps')
)

install_data(
    join_paths(actions_dir, 'sideload-package-symbolic.svg'),
    install_dir: join_paths(get_option('datadir'), 'icons', 'hicolor', 'scalable', 'actions')
)