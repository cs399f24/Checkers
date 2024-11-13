# Checkers Game Deployment

An online Checkers game that utilizes AWS resources for hosting and storage.

## Contributors

- **Jeffery Eisenhardt** - [eisenhardtj](https://github.com/eisenhardtj)
- **Trevor Gray** - [trevor-gray17](https://github.com/trevor-gray17)
- **Brandon Yang** - [CloudUki](https://github.com/CloudUki)
- **Nathaniel Hajel** - [nateh17](https://github.com/nateh17)

---

## Deployment Instructions

### 1. Launch an EC2 Instance

1. **Log in to AWS**: Go to [AWS Management Console](https://aws.amazon.com) and sign in.
2. **Navigate to EC2**: Use the search bar to find and access the EC2 Dashboard.
3. **Launch a New Instance**:
   - Click "Launch Instance" and select **Amazon Linux 2 AMI**.
   - Choose `t2.micro` (free tier eligible) as the instance type.
4. **Configure Security Group**:
   - Allow **SSH** (Port 22) for remote access.
   - Allow **HTTP** (Port 80) for web traffic.
   - Add an inbound rule for **Port 8080** (used by the application server).
5. **Review and Launch**: Confirm settings, then launch. Download the key pair (.pem file) when prompted and store it securely.

### 2. Connect to Your EC2 Instance

1. **Open a Terminal** on your local machine.
2. **Navigate to the Key Pair**: Change to the directory where the `.pem` file is stored:
   ```sh
   cd path/to/your-key-pair
