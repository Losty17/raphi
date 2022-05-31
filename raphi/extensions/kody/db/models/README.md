# Schema

## Tables

### Bits

| bit_name | bit_id |
|----------|--------|
| web      |    0   |
| data     |    1   |
| design   |    2   |
| coding   |    3   |
| network  |    4   |
| robotics |    5   |
| hardware |    6   |
| software |    7   |

### User

| id | vip |
|----|-----|
| 0  |none |

### User Bits

| ref_user | ref_bit | qty |
|----------|---------|-----|
|    0     |    0    | 64  |
|    0     |    1    | 32  |
|    0     |    2    | 16  |
|    0     |    3    | 8   |
|    0     |    4    | 4   |
|    0     |    5    | 2   |
|    0     |    6    | 1   |
|    0     |    7    | 0   |

#### Example query for bits

    SELECT * FROM user_bits WHERE ref_user = user.id AND ref_bit = node.value
