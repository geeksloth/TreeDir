def treedir(dir_path, level: int=-1, limit_to_directories: bool=False, length_limit: int=200):
	# I modified the official pathlib library to ignore some system directory to avoid the access deny error.
	# Alternately, you can change it to use the official one with latest update instead, eg, from pathlib import Path
	from mypathlib import Path
	from itertools import islice
	space =  '    '
	branch = '│   '
	tee =    '├── '
	last =   '└── '
	print(dir_path)
	dir_path = Path(dir_path)
	files = 0
	directories = 0
	def inner(dir_path: Path, prefix: str='', level=-1):
		nonlocal files, directories
		if not level: 
			return
		if limit_to_directories:
			contents = [d for d in dir_path.iterdir() if d.is_dir()]
		else: 
			contents = list(dir_path.iterdir())
		pointers = [tee] * (len(contents) - 1) + [last]
		for pointer, path in zip(pointers, contents):
			if path.is_dir():
				yield prefix + pointer + path.name
				directories += 1
				extension = branch if pointer == tee else space 
				try:
					yield from inner(path, prefix=prefix+extension, level=level-1)
				except KeyError:
					pass
			elif not limit_to_directories:
				yield prefix + pointer + path.name
				files += 1
	iterator = inner(dir_path, level=level)
	for line in islice(iterator, length_limit):
		print(line)
	if next(iterator, None):
		print(f'... length_limit, {length_limit}, reached, counted:')
	#print(f'\n{directories} directories' + (f', {files} files' if files else ''))

