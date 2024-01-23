from eth_abi import encode

# Define the data types as strings
order_info_type = "(address,address,uint256,uint256,address,bytes)"
partial_input_type = "(address,uint256)"
partial_output_type = "(address,uint256,address)"
partial_order_type = "(tuple,address,uint256,tuple,tuple[])"

# Define the data structure with correct types
partial_order_abi = [
    order_info_type,  # OrderInfo
    "address",  # exclusiveFiller
    "uint256",  # exclusivityOverrideBps
    partial_input_type,  # PartialInput
    partial_output_type + "[]",  # PartialOutput[]
]

# Define your data
order_info_values = (
    "0x0B94c1A3E11F8aaA25D27cAf8DD05818e6f2Ad97",
    "0x8fd379246834eac74B8419FfdA202CF8051F7A03",
    1000,  # Non-hexadecimal uint256
    1709071200,  # Non-hexadecimal uint256
    "0x0000000000000000000000000000000000000000",
    b"",  # Empty bytes
)

partial_input_values = (
    "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",
    40000000000000000000,  # Non-hexadecimal uint256
)

partial_output_values = [
    (
        "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
        34600000,  # Non-hexadecimal uint256
        "0x8fd379246834eac74B8419FfdA202CF8051F7A03",
    )
]

exclusive_filler = "0x1a08D64Fb4a7D0b6DA5606A1e4619c147C3fB95e"
exclusivity_override_bps = 0  # Non-hexadecimal uint256

partial_order_values = (
    order_info_values,
    exclusive_filler,
    exclusivity_override_bps,
    partial_input_values,
    partial_output_values,
)

# Encode the data using the defined ABI
encoded_data = encode(partial_order_abi, partial_order_values)

breakpoint()

print(encoded_data.hex())
print("Length: ", len(encoded_data.hex()))
