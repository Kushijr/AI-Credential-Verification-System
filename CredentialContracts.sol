pragma solidity ^0.8.0;

contract CredentialContract {

    string public credential;

    function storeCredential(
        string memory _credential
    ) public {

        credential = _credential;
    }

    function getCredential()
        public
        view
        returns(string memory)
    {

        return credential;
    }
}