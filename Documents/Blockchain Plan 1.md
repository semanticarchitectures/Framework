# Remove all .DS_Store files from Git tracking
find . -name .DS_Store -print0 | xargs -0 git rm --ignore-unmatch --cached

# Delete actual .DS_Store files
find . -name .DS_Store -delete
