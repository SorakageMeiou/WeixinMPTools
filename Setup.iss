[Setup]
AppId={{A1B2C3D4-E5F6-7890-1234-567890ABCDEF}
AppName=WeixinMPTools
AppVersion=1.0.0
AppVerName=WeixinMPTools v1.0
AppPublisher=SoraKaGe_MeiOu
AppPublisherURL=https://github.com/SorakageMeiou
AppSupportURL=https://github.com/SorakageMeiou/issues
AppUpdatesURL=https://github.com/SorakageMeiou/releases
AppCopyright=Copyright (c) 2024 SoraKaGe_MeiOu. All rights reserved.

; 安装目录设置
DefaultDirName={autopf}\SoraKaGe_MeiOu\WeixinMPTools
DefaultGroupName=WeixinMPTools
AllowNoIcons=yes
DisableProgramGroupPage=no

; 输出设置
OutputDir=Output
OutputBaseFilename=WeixinMPTools_Setup_v1.0
SetupIconFile=Assets\icon.ico
UninstallDisplayIcon={app}\WeixinMPTools.exe
UninstallDisplayName=WeixinMPTools

; 压缩设置
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=4

; 界面设置
WizardStyle=modern
WizardSizePercent=110,120
WizardResizable=yes
WizardImageFile=Assets\WizardImage.bmp
WizardSmallImageFile=Assets\WizardSmallImage.bmp
SetupLogging=yes

; 权限设置
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Messages]
chinesesimplified.BeveledLabel=WeixinMPTools - 让公众号运营更高效

[CustomMessages]
chinesesimplified.MyDescription=一款功能强大的公众号运营辅助工具
chinesesimplified.AdditionalIcons=附加图标选项：
chinesesimplified.CreateDesktopIcon=创建桌面快捷方式 (&D)
chinesesimplified.CreateQuickLaunchIcon=创建快速启动栏快捷方式 (&Q)
chinesesimplified.LaunchProgram=启动WeixinMPTools (&L)

[Types]
Name: "full"; Description: "完全安装"
Name: "compact"; Description: "精简安装"
Name: "custom"; Description: "自定义安装"; Flags: iscustom

[Components]
Name: "main"; Description: "主程序文件"; Types: full compact custom; Flags: fixed
Name: "resources"; Description: "资源文件"; Types: full
Name: "docs"; Description: "说明文档"; Types: full

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Components: main
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Components: main; Flags: unchecked
Name: "autostart"; Description: "开机自动启动"; GroupDescription: "其他任务:"; Flags: unchecked

[Files]
; 主程序文件
Source: "dist\WeixinMPTools.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: main
Source: "Assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion; Components: main

; 资源文件
Source: "Assets\*"; DestDir: "{app}\Assets"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: resources

; 文档文件
;Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion; Components: docs

[Icons]
; 开始菜单图标
Name: "{group}\WeixinMPTools"; Filename: "{app}\WeixinMPTools.exe"; IconFilename: "{app}\icon.ico"; Comment: "公众号运营辅助工具"
Name: "{group}\{cm:UninstallProgram,WeixinMPTools}"; Filename: "{uninstallexe}"

; 桌面图标
Name: "{autodesktop}\WeixinMPTools"; Filename: "{app}\WeixinMPTools.exe"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"

; 快速启动图标
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\WeixinMPTools"; Filename: "{app}\WeixinMPTools.exe"; Tasks: quicklaunchicon; IconFilename: "{app}\icon.ico"

; 开机启动图标
Name: "{commonstartup}\WeixinMPTools"; Filename: "{app}\WeixinMPTools.exe"; Tasks: autostart

[Registry]
; 应用设置
Root: HKA; Subkey: "Software\SoraKaGe_MeiOu\WeixinMPTools"; Flags: uninsdeletekey

[Run]
; 安装后运行
Filename: "{app}\WeixinMPTools.exe"; Description: "{cm:LaunchProgram}"; Flags: nowait postinstall skipifsilent unchecked
Filename: "https://github.com/SorakageMeiou"; Description: "访问项目主页"; Flags: shellexec postinstall skipifsilent unchecked
; Filename: "{app}\README.md"; Description: "查看说明文档"; Flags: shellexec postinstall skipifsilent unchecked; Components: docs

; 安装运行库（如果需要）
; Filename: "{app}\vcredist_setup.exe"; Parameters: "/install /quiet /norestart"; StatusMsg: "正在安装运行库..."

[UninstallRun]
; Filename: "{app}\WeixinMPTools.exe"; Parameters: "--uninstall"; Flags: runhidden waituntilterminated

[UninstallDelete]
Type: filesandordirs; Name: "{app}\Logs"
Type: filesandordirs; Name: "{app}\Temp"
Type: files; Name: "{app}\*.log"

[Code]
// 初始化向导
procedure InitializeWizard;
begin
  // 可以在这里添加自定义界面元素
end;

// 下一步按钮点击事件 - 添加路径验证
function NextButtonClick(CurPageID: Integer): Boolean;
var
  InstallPath: string;
begin
  Result := True;
  
  if CurPageID = wpSelectDir then
  begin
    InstallPath := WizardForm.DirEdit.Text;
    
    // 检查路径是否有效
    if InstallPath = '' then
    begin
      MsgBox('请选择安装路径或点击"默认路径"按钮。', mbError, MB_OK);
      Result := False;
      Exit;
    end;
  end;
end;

// 自定义安装过程
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // 安装完成后的操作
  end;
end;

function InitializeUninstall(): Boolean;
begin
  Result := True;

end;
