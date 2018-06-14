# -*- mode: python -*-

block_cipher = None


a = Analysis(['count_code_lines_git.py'],
             pathex=['/Users/hjh/PycharmProjects/CountCodeLines'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='count_code_lines_git',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='count_code_lines_git')
app = BUNDLE(coll,
             name='count_code_lines_git.app',
             icon=None,
             bundle_identifier=None)
