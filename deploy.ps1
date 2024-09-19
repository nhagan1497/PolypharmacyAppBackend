$filesToZip = Get-ChildItem -Path . -Exclude .*
$filesToZip | Compress-Archive -DestinationPath output.zip

az webapp deploy --name PolypharmacyAppBackend --resource-group PolypharmacyAppResourceGroup --src-path output.zip
rm output.zip