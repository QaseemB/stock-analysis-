export 
PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:$PATH"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/qaseembarnhardt/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/qaseembarnhardt/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/qaseembarnhardt/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/qaseembarnhardt/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<


PATH=~/.console-ninja/.bin:$PATHexport PATH="/Library/PostgreSQL/17/bin:$PATH"
