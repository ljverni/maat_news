# -------------------------------
# Lambda Packaging Script with Parameter
# -------------------------------

param (
    [string]$LambdaName = "the_guardian"   # default value if none provided
)

# 1️⃣ Define variables
$projectRoot = "C:\Users\Luciano\Documents\projects\maat_news"
$packageDir = "$projectRoot\package"
$zipFile = "$projectRoot\$LambdaName.zip"
$handlerFile = "\lambdas\$LambdaName\lambda_function.py"
$helpersFolder = "helpers"
$requirementsFile = "requirements.txt"

# 2️⃣ Clean previous package and ZIP
if (Test-Path $packageDir) { Remove-Item $packageDir -Recurse -Force }
if (Test-Path $zipFile) { Remove-Item $zipFile -Force }

# 3️⃣ Create package folder
New-Item -ItemType Directory -Path $packageDir

# 4️⃣ Install dependencies into package
python -m pip install --upgrade pip
python -m pip install -r "$projectRoot\$requirementsFile" -t $packageDir

# 5️⃣ Copy Lambda handler
Copy-Item "$projectRoot\$handlerFile" $packageDir\

# 6️⃣ Copy helpers folder
xcopy "$projectRoot\$helpersFolder" "$packageDir\$helpersFolder" /E /I

# 7️⃣ Create ZIP file
cd $packageDir
tar -a -c -f $zipFile *

# 8️⃣ Done
Write-Output "✅ Lambda ZIP created: $zipFile"
