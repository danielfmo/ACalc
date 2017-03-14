#define MyAppName "ACalc"
#define MyAppServerName "ACalc Server"
#define MyAppPublisher "Daniel Oliveira"
#define MyAppExeName "ACalc.exe"
#define MyConfigName "Settings"
#define MyConfigExeName "server.ini"
#define MyAppURL "http://localhost:8080/"

[Setup]
AppID={code:GetAppID|''}
AppName={#MyAppName}
AppVersion={code:GetAppVersion|''}
AppVerName={#MyAppName} {code:GetAppVersion|''} build {code:GetAppBuild|''}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=SETUP
OutputBaseFilename={#MyAppName}-update
Compression=lzma
SolidCompression=yes
UsePreviousLanguage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; 

[Files]
Source: "C:\Acalc_Server\build\exe.win32-3.3\ACalc.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Acalc_Server\build\exe.win32-3.3\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "version.dat"; DestDir: "{tmp}"; Flags: dontcopy
Source: "build.dat"; DestDir: "{tmp}"; Flags: dontcopy

[Icons]
Name: "{group}\{#MyAppServerName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{#MyAppServerName}"; Filename: "{app}\{#MyAppURL}"
Name: "{group}\{#MyConfigName}"; Filename: "{app}\conf\{#MyConfigExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppServerName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyConfigName}"; Filename: "{app}\conf\{#MyConfigExeName}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyAppName}"; Filename: "{#MyAppURL}"; Tasks: desktopicon

;[Run]
;Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked

[UninstallDelete]
Type: files; Name: "{app}\{#MyAppExeName}"

[Registry]
Root: HKLM; Subkey: Software\{#MyAppName}; ValueType: string; ValueName: Version; ValueData: {code:GetAppVersion|''}; Flags: uninsdeletekey createvalueifdoesntexist
Root: HKLM; Subkey: Software\{#MyAppName}; ValueType: string; ValueName: Build; ValueData: {code:GetAppBuild|''}; Flags: uninsdeletekey

[Code]
function GetAppID(param: String): String;
	begin
		Result := 'ACalc';
	end;
	
function GetAppVersion(param: String): String;
	var
		AppVersion: String;
	begin
		ExtractTemporaryFile('version.dat');
		LoadStringFromFile(ExpandConstant('{tmp}\version.dat'), AppVersion);
		Result := AppVersion;
	end;
	
function GetAppBuild(param: String): String;
	var
		BuildVersion: String;
	begin
		ExtractTemporaryFile('build.dat');
		LoadStringFromFile(ExpandConstant('{tmp}\build.dat'), BuildVersion);
		Result := BuildVersion;
	end;

function GetPathInstalled(AppID: String): String;
	var
		PrevPath: String;
	begin
		PrevPath := '';
		if not RegQueryStringValue(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\'+AppID+'_is1', 'Inno Setup: App Path', PrevPath) then begin
			RegQueryStringValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\'+AppID+'_is1', 'Inno Setup: App Path', PrevPath);
		end;
		Result := PrevPath;
	end;

function GetInstalledVersion(): String;
	var
		InstalledVersion: String;
	begin
		InstalledVersion := '';
		RegQueryStringValue(HKLM, 'Software\{#MyAppName}', 'Version', InstalledVersion);
		Result := InstalledVersion;
	end;

function GetInstalledBuild(): String;
	var
		InstalledBuild: String;
	begin
		InstalledBuild := '';
		RegQueryStringValue(HKLM, 'Software\{#MyAppName}', 'Build', InstalledBuild);
		Result := InstalledBuild;
	end;

function InitializeSetup(): Boolean;
	var
		Response: Integer;
		PrevDir: String;
		InstalledVersion: String;
		InstalledBuild: String;
		VersionError: String;
	begin
		Result := true;

		// read the installtion folder
		PrevDir := GetPathInstalled(getAppID(''));

		if length(Prevdir) > 0 then begin
			// I found the folder so it's an upgrade
			InstalledVersion := GetInstalledVersion();
			// compare versions
			if InstalledVersion = GetAppVersion('') then begin
				InstalledBuild := GetInstalledBuild();
				if (InstalledBuild < GetAppBuild('')) then begin
					Result := True;
				end else if (InstalledBuild = GetAppBuild('')) then begin
					Response := MsgBox(
						'It appears that the existing {#MyAppName} installation is already current.' + #13#13 +
						'Do you want to continue with the update installation?', mbError, MB_YESNO
					);
					Result := (Response = IDYES);
				end else begin
					Response := MsgBox(
						'It appears that the existing {#MyAppName} installation newer than this update.' + #13#13 +
						'The existing installation is build '+ InstalledBuild +'.  This update will change the installation to build '+ GetAppBuild('') + #13#13 +
						'Do you want to continue with the update installation?', mbError, MB_YESNO
					);
					Result := (Response = IDYES);
				end;
			end else begin
				if length(InstalledVersion) = 0 then begin
					VersionError := 'Setup was unable to determine the version of the existing {#MyAppName} installation.';
				end else begin
					VersionError := 'Setup has detected an installation of {#MyAppName} ' + InstalledVersion + '.';
				end;
				MsgBox(
					VersionError + #13#13 +
					'This update installer requires {#MyAppName} ' + GetAppVersion('') +' to ' +
					'already be installed.' + #13 + 'Please install {#MyAppName} ' + GetAppVersion('') +' before running this update.' + #13#13 +
					'Setup/Upgrade aborted.', mbError, MB_OK
				);
				Result := false;
			end;
		end else begin
			MsgBox(
				'This update installer requires an existing installation of {#MyAppName} ' + GetAppVersion('') +' to ' +
				'already be installed.' + #13 + 'Please install {#MyAppName} ' + GetAppVersion('') +' before running this update.' + #13#13 +
				'Setup/Upgrade aborted.', mbError, MB_OK
			);
			Result := false;
		end;
    end;

function ShouldSkipPage(PageID: Integer): Boolean;
	begin
		// skip selectdir if It's an upgrade
		if (PageID = wpSelectDir) then begin
			Result := true;
		end else if (PageID = wpSelectProgramGroup) then begin
			Result := true;
		end else if (PageID = wpSelectTasks) then begin
			Result := true;
		end else begin
			Result := false;
		end;
	end;
