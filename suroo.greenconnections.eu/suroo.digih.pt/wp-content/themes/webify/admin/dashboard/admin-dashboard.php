<?php
/**
* Admin Dashboard
*/
if( !defined( 'ABSPATH' ) ) exit; // Exit if accessed directly

if(!class_exists('Webify_Admin_Dashboard')) {
  class Webify_Admin_Dashboard {
    function __construct() {
      $this->webify_init();
    }

    public function webify_init() {
      add_action('admin_menu', array($this, 'webify_register_theme_panel'));
      add_action('admin_init', array($this, 'webify_theme_redirect'));
    }

    public function webify_register_theme_panel() {
      call_user_func('add_'. 'menu' .'_page', esc_html__('Theme Panel', 'webify'), esc_html__('Webify', 'webify'), 'edit_posts', 'webify_theme_welcome', array($this, 'webify_view_welcome'), null, 2);
      call_user_func( 'add_'. 'submenu' .'_page', 'webify_theme_welcome', esc_html__('Help Center', 'webify'), esc_html__('Help Center', 'webify'), 'edit_posts', 'webify_theme_help_center', array($this, 'webify_theme_help_center'));
      global $submenu;
      $submenu['webify_theme_welcome'][0][0] = esc_html__('Welcome', 'webify');
    }

    public function webify_view_welcome() {
      require_once 'welcome.php';
    }
    
    public function webify_theme_help_center() {
      require_once 'help-center.php';
    }

    public function webify_theme_redirect() {
      global $pagenow;
      if ( is_admin() && isset( $_GET['activated'] ) && 'themes.php' == $pagenow ) {
        wp_redirect(admin_url('admin.php?page=webify_theme_welcome')); 
      }
    }
  }
  new Webify_Admin_Dashboard();
}
