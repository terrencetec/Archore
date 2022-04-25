"vim-plug stuff
let data_dir = has('nvim') ? stdpath('data') . '/site' : '~/.vim'
if empty(glob(data_dir . '/autoload/plug.vim'))
  silent execute '!curl -fLo '.data_dir.'/autoload/plug.vim --create-dirs  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif


"vim-plug call plugins
call plug#begin('~/.vim/plugged')

"Syntax color scheme
Plug 'joshdick/onedark.vim'

"Syntax highlighting
Plug 'sheerun/vim-polyglot'
"Plug 'vim-python/python-syntax'

"NERDTree
Plug 'scrooloose/nerdtree'
"Plug 'scrooloose/nerdtree-project-plugin'
Plug 'Xuyuanp/nerdtree-git-plugin'
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'

" Auto comment
"Plug 'KarimElghamry/vim-auto-comment'
"Plug 'preservim/nerdcommenter'
Plug 'tpope/vim-commentary'

"Vim session
Plug 'xolox/vim-session'
Plug 'xolox/vim-misc'

"VimWiki
Plug 'vimwiki/vimwiki'

call plug#end()


"Basic stuff
set colorcolumn=80
set encoding=utf-8
set number
set mouse=a
set splitbelow splitright 
filetype plugin on


"Syntax highlighting
"Use 24-bit (true-color) mode in Vim/Neovim when outside tmux.
"If you're using tmux version 2.2 or later, you can remove the outermost $TMUX check and use tmux's 24-bit color support
"(see < http://sunaku.github.io/tmux-24bit-color.html#usage > for more information.)
if (empty($TMUX))
  if (has("nvim"))
    "For Neovim 0.1.3 and 0.1.4 < https://github.com/neovim/neovim/pull/2198 >
    let $NVIM_TUI_ENABLE_TRUE_COLOR=1
  endif
  "For Neovim > 0.1.5 and Vim > patch 7.4.1799 < https://github.com/vim/vim/commit/61be73bb0f965a895bfb064ea3e55476ac175162 >
  "Based on Vim patch 7.4.1770 (`guicolors` option) < https://github.com/vim/vim/commit/8a633e3427b47286869aa4b96f2bfc1fe65b25cd >
  " < https://github.com/neovim/neovim/wiki/Following-HEAD#20160511 >
  if (has("termguicolors"))
    set termguicolors
  endif
endif
syntax on
colorscheme onedark
hi Normal guibg=NONE ctermbg=NONE
hi Todo guifg=red
hi Terminal guibg=NONE ctermbg=NONE
"highlight ColorColumn guibg=lightgray
"let g:python_highlight_all = 1

"Moving across windows
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l
map <C-left> <C-w>h
map <C-down> <C-w>j
map <C-up> <C-w>k
map <C-right> <C-w>l

"NERTree stuff
"NERDTree Toggle
map <C-t> : NERDTreeToggle<CR> 

"Start NERDTree
autocmd VimEnter * NERDTree
let NERDTreeShowBookmarks=1

"Keep NERDTree open on new tabs
autocmd BufWinEnter * NERDTreeMirror


"Save session
let g:session_autosave='yes'
"let g:session_autosave_periodic=1
let g:session_autoload='yes'
" let g:session_lock_enabled = 0
" autocmd VimEnter * OpenSession


"Auto comment
let g:inline_comment_dict = {
		\'//': ['js', 'ts', 'cpp', 'c', 'dart'],
		\'#': ['py', 'sh'],
		\'"': ['vim'],
		\}

"Clipboard
"set clipboard=unnamedplus

"VimWiki stuff
let g:vimwiki_list = [{'path': '~/Dropbox/vimwiki/'}]
