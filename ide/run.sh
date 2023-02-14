#!/bin/bash
echo "



    for brave goto brave://flags/  search for file-system-access-api and enable



"

if [ -f "/opt/appimage/Chromium.AppImage" ]
then
    BROWSER=/opt/appimage/Chromium.AppImage
else 
    wget -c https://apprepo.de/appimage/download/chromium --output-document=ide/Chromium.AppImage
    chmod +x ./ide/Chromium.AppImage
    BROWSER=$(pwd)/ide/Chromium.AppImage
fi


$BROWSER \
 --password-store=basic  --disable-cookie-encryption --user-data-dir=$(pwd)/ide/webdev.pro \
 --no-default-browser-check --test-type  --auto-open-devtools-for-tabs \
 --aggressive-cache-discard --disable-notifications --disable-remote-fonts \
 --disable-voice-input --enable-aggressive-domstorage-flushing --disable-shared-workers \
 --disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies \
 --enable-features=Vulkan,file-system-access-api --enable-unsafe-webgpu --enable-webgpu-developer-feature \
 http://localhost:8000

