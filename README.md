# COMP3900 Project 

This is the P133 project _Systems and Methods for Phishing and Spam Detection_


### <u>Run project via docker (Most portable)</u>

#### Run entire stack:
```bash
docker compose up --build
```

### Run project locally (Easiest way to debug)

#### Front end:
```bash
cd frontend
npm run dev
```

#### Back end:
```bash
python3 backend/app.py
```

#### Run database:
```bash
docker compose -f 'docker-compose.yml' up -d --build 'db' 
```

## Usage

TODO:
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.



## License

[MIT](https://choosealicense.com/licenses/mit/)
```

## Authors
Joules, Ray, Kelly, Lara, Shadab, Caitlin