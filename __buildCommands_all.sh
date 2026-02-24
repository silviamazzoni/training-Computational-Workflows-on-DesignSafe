pip install jupyter-book

python -m pip install sphinx-last-updated-by-git
python -c "import sphinx_last_updated_by_git; print('ok')"


# pip install OpenSeesPy

# cd ~/MyData/_ToCommunityData/OpenSees/TrainingMaterial/training-OpenSees-on-DesignSafe

### jupyter-book clean . --all; python generate_md_toc.py ; jupyter-book build .

now:

./build_all_books.sh

./build_all_books.sh --preprompt --clean


./build_all_books.sh --preprompt --clean --gen-md-toc



