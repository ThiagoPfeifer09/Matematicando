[app]
title = Matematicando
package.name = matemas
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv
version = 0.1
requirements = python3,kivy,kivymd,matplotlib,kivy_garden.matplotlib
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.target = android-33
# no buildozer.spec
android.permissions = BLUETOOTH
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 0
