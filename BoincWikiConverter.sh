wiki_files=(
    "AppFiltering"
    "AppPlan"
    "AppPlanSpec"
    "AppVersion"
    "AppVersionNew"
    "BackendPrograms"
    "BasicApi"
    "BetaTest"
    "BoincFiles"
    "BuildMacApp"
    "CloudServer"
    "CodeSigning"
    "CompileApp"
    "CompileAppWin"
    "DataBase"
    "DeleteFile"
    "DesktopGrid"
    "ExampleApps"
    "FileCompression"
    "GraphicsApi"
    "GraphicsApps"
    "HomogeneousRedundancy"
    "HTMLGfx"
    "HtmlOps"
    "IntermediateUpload"
    "JobEst"
    "JobIn"
    "JobStage"
    "JobSubmission"
    "JobTemplates"
    "KeySetup"
    "LocalityNew"
    "LocalityScheduling"
    "MakeProject"
    "MultiHost"
    "PlanClassFunc"
    "ProfileScreen"
    "ProjectConfigFile"
    "ProjectOptions"
    "ServerComponents"
    "ServerIntro"
    "SourceCodeGit"
    "SourceCodeGit/Windows"
    "VboxApps"
    "VolunteerComputing"
    "WorkGeneration"
    "XmlFormat"
)

declare -A pages_from_subdirectories
pages_from_subdirectories["SourceCodeGit/Windows"]="SourceCodeGit_Windows"

for wiki_file in "${wiki_files[@]}"
do
    url=${wiki_file}
    if [ -v pages_from_subdirectories[$wiki_file] ]; then
        file=${pages_from_subdirectories[$wiki_file]}
    else
        file=${wiki_file}
    fi

    if [ ! -f "/c/Users/Vitalii.Koshura/Downloads/${file}.txt" ]; then
        echo "Downloading ${wiki_file}..."
        curl -o "/c/Users/Vitalii.Koshura/Downloads/${file}.txt" "https://boinc.berkeley.edu/trac/wiki/${wiki_file}?format=txt"
    fi
    python "./wiki2md.py" "/c/Users/Vitalii.Koshura/Downloads/${file}.txt" "/c/SRC/Other/boinc.wiki/${file}.md"
done

declare -A wiki_images

wiki_images["SourceCodeGit/Windows/file-list.png"]="file-list.png"
wiki_images["SourceCodeGit/Windows/git-1.png"]="git-1.png"
wiki_images["SourceCodeGit/Windows/git-2.png"]="git-2.png"
wiki_images["SourceCodeGit/Windows/git-3.png"]="git-3.png"
wiki_images["SourceCodeGit/Windows/git-4.png"]="git-4.png"
wiki_images["SourceCodeGit/Windows/git-5.png"]="git-5.png"
wiki_images["SourceCodeGit/Windows/tortoisegit-1.png"]="tortoisegit-1.png"
wiki_images["SourceCodeGit/Windows/tortoisegit-2.png"]="tortoisegit-2.png"
wiki_images["SourceCodeGit/Windows/tortoisegit-3.png"]="tortoisegit-3.png"
wiki_images["CompileAppWin/runtimerror.png"]="runtimerror.png"

for url in "${!wiki_images[@]}"
do
    file=${wiki_images[$url]}
    if [ ! -f "/c/Users/Vitalii.Koshura/Downloads/${file}" ]; then
        echo "Downloading ${url}..."
        curl -o "/c/Users/Vitalii.Koshura/Downloads/${file}" "https://boinc.berkeley.edu/trac/raw-attachment/wiki/${url}"
    fi
    cp "/c/Users/Vitalii.Koshura/Downloads/${file}" "/c/SRC/Other/boinc.wiki/${file}"
done
