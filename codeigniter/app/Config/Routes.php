<?php

use CodeIgniter\Router\RouteCollection;

/**
 * @var RouteCollection $routes
 */
 $routes->get('/', 'Home::index');
// $routes->get('demo', 'Home::demo');
$routes->get('main/', 'Home::main');

service('auth')->routes($routes);
