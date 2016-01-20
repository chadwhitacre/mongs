env:
	unzip -q -d vendor/virtualenv vendor/virtualenv*.whl
	python ./vendor/virtualenv/virtualenv.py \
				--prompt="[mongs] " \
				./env/
	rm -R vendor/virtualenv
	./env/bin/pip install -r requirements.txt

clean:
	rm -rf env

run: env
	PORT=29017 env/bin/python launch.py
