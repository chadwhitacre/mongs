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
	./env/bin/aspen --network_address=127.0.0.1:29017 \
				    --www_root=www/ \
					--project_root=.
