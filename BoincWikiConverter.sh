wiki_files=(
    "AdaptiveReplication"
    "AndroidBuildApp"
    "AppCoprocessor"
    "AppFiltering"
    "AppMultiThread"
    "AppPlan"
    "AppPlanSpec"
    "AppVersion"
    "AppVersionNew"
    "AssignedWork"
    "BackendPrograms"
    "BackendUtilities"
    "BasicApi"
    "BetaTest"
    "BoincFiles"
    "BoincPlatforms"
    "BuildMacApp"
    "BuildSystem"
    "CloudServer"
    "CodeSigning"
    "CompileApp"
    "CompileAppLinux"
    "CompileAppWin"
    "CreditAlt"
    "CreditNew"
    "CreditOptions"
    "DataBase"
    "DbPurge"
    "DeleteFile"
    "DesktopGrid"
    "EmailLists"
    "ExampleApps"
    "FileCompression"
    "FileDeleter"
    "GPUApp"
    "GraphicsApi"
    "GraphicsApps"
    "HomogeneousRedundancy"
    "HTMLGfx"
    "HtmlOps"
    "IntermediateUpload"
    "JobEst"
    "JobIn"
    "JobReplication"
    "JobStage"
    "JobSubmission"
    "JobTemplates"
    "KeySetup"
    "LocalityNew"
    "LocalityScheduling"
    "MacBuild"
    "MakeProject"
    "MultiHost"
    "MultiSize"
    "OpenclApps"
    "PhysicalFileManagement"
    "PlanClassFunc"
    "ProfileScreen"
    "ProjectConfigFile"
    "ProjectDaemons"
    "ProjectOptions"
    "ProjectPeople"
    "PythonMysql"
    "ServerComponents"
    "ServerIntro"
    "SoftwarePrereqsUnix"
    "SourceCodeGit"
    "SourceCodeGit/Windows"
    "StartTool"
    "TrickleApi"
    "TrickleMessages"
    "UpdateVersions"
    "ValidationIntro"
    "ValidationSimple"
    "VboxApps"
    "VersionPathSorter"
    "VirtualBox"
    "VmApps"
    "VmCompatibility"
    "VolunteerComputing"
    "WorkGeneration"
    "WrapperApp"
    "XaddTool"
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
wiki_images["VmApps/Wrapper_VM_Ben.rtf"]="Wrapper_VM_Ben.rtf"
wiki_images["VmApps/boinc_vmware.pdf"]="boinc_vmware.pdf"
wiki_images["VmApps/wrapperWeir.cpp"]="wrapperWeir.cpp"
wiki_images["VmApps/BOINCandVM.png"]="BOINCandVM.png"
wiki_images["VirtualBox/STOMPArchV2.png"]="STOMPArchV2.png"
wiki_images["VirtualBox/classDiagram.png"]="classDiagram.png"

for url in "${!wiki_images[@]}"
do
    file=${wiki_images[$url]}
    if [ ! -f "/c/Users/Vitalii.Koshura/Downloads/${file}" ]; then
        echo "Downloading ${url}..."
        curl -o "/c/Users/Vitalii.Koshura/Downloads/${file}" "https://boinc.berkeley.edu/trac/raw-attachment/wiki/${url}"
    fi
    cp "/c/Users/Vitalii.Koshura/Downloads/${file}" "/c/SRC/Other/boinc.wiki/${file}"
done
